import enum
import os
from typing import Any, Optional
from bcml.core.game_data import cat_base
from bcml.core import io, country_code, crypto, anim


class BCUFileGroup:
    def __init__(self, bcu_files: list["BCUFile"]) -> None:
        """
        Initialize a BCUFileGroup object.

        Args:
            bcu_files (list[BCUFile]): The list of BCU files.
        """
        self.bcu_files = bcu_files

    def get_file_by_name(self, name: str) -> Optional["BCUFile"]:
        """
        Get a BCU file by name.

        Args:
            name (str): The name of the file.

        Returns:
            Optional[BCUFile]: The BCU file.
        """
        for bcu_file in self.bcu_files:
            if bcu_file.name == name:
                return bcu_file
        return None

    def get_files_by_prefix(self, prefix: str) -> list["BCUFile"]:
        """
        Get a list of BCU files by prefix.

        Args:
            prefix (str): The prefix of the file.

        Returns:
            list[BCUFile]: The list of BCU files.
        """
        files: list[BCUFile] = []
        for bcu_file in self.bcu_files:
            if bcu_file.name.startswith(prefix):
                files.append(bcu_file)
        return files


class BCUForm:
    def __init__(
        self,
        form_data: dict[str, Any],
        anims: "BCUFileGroup",
    ):
        self.form_data = form_data
        self.id = self.form_data["anim"]["id"]
        self.name = self.form_data["names"]["dat"][0]["val"]
        self.description = self.form_data["description"]["dat"][0]["val"].split("<br>")
        self.anims = anims
        anim = self.load_anim()
        if anim is None:
            return None
        self.anim = anim
        cat_id_form = self.get_cat_id_form()
        if cat_id_form is None:
            self.cat_id = -1
            self.form = cat_base.cats.FormType.FIRST
        else:
            self.cat_id, self.form = cat_id_form

        upgrade_icon = self.load_display_icon()
        if upgrade_icon is None:
            return None
        self.upgrade_icon = upgrade_icon

        deploy_icon = self.load_deploy_icon()
        if deploy_icon is None:
            return None
        self.deploy_icon = deploy_icon

    def get_cat_id_form(self) -> Optional[tuple[int, "cat_base.cats.FormType"]]:
        img_name = self.anim.imgcut.image_name
        cat_id = int(img_name[:3])
        form_str = img_name[4:5]
        try:
            form_type = cat_base.cats.FormType(form_str)
        except ValueError:
            return None
        return cat_id, form_type

    def load_anim(self) -> Optional["anim.bc_anim.Model"]:
        sprite = self.anims.get_file_by_name("sprite.png")
        imgcut = self.anims.get_file_by_name("imgcut.txt")
        mamodel = self.anims.get_file_by_name("mamodel.txt")
        maanims = self.anims.get_files_by_prefix("maanim")
        if sprite is None or imgcut is None or mamodel is None:
            return None
        image = io.bc_image.BCImage(sprite.data)
        imgcut = anim.bc_anim.Imgcut.from_data(imgcut.data, image)
        mamodel = anim.bc_anim.Mamodel.from_data(mamodel.data, imgcut.cuts)
        maanims = [
            anim.bc_anim.Maanim.from_data(maanim.data, maanim.name)
            for maanim in maanims
        ]
        return anim.bc_anim.Model(imgcut, mamodel, maanims)

    def load_display_icon(self) -> Optional["io.bc_image.BCImage"]:
        display_file = self.anims.get_file_by_name("icon_display.png")
        if display_file is None:
            return None

        display_image = io.bc_image.BCImage(display_file.data)
        display_image.scale(3.5, 3.5)

        base_image = io.bc_image.BCImage.from_size(512, 128)
        base_image.paste(display_image, 13, 1)

        start_pos = (146, 112)
        end_pos = (118, 70)
        start_offset = 0
        start_width = 311 - start_pos[0]
        for i in range(start_pos[1] - end_pos[1]):
            for j in range(start_width):
                base_image.putpixel(
                    start_pos[0] + j + start_offset, start_pos[1] - i, (0, 0, 0, 0)
                )
            start_offset += 1
            start_width -= 1

        return base_image

    def load_deploy_icon(self) -> Optional["io.bc_image.BCImage"]:
        deploy_file = self.anims.get_file_by_name("icon_deploy.png")
        if deploy_file is None:
            return None

        deploy_image = io.bc_image.BCImage(deploy_file.data)

        base_image = io.bc_image.BCImage.from_size(128, 128)
        base_image.paste(deploy_image, 9, 21)
        return base_image

    def get_cat_id_str(self):
        return io.data.PaddedInt(self.cat_id, 3).to_str()

    def to_cat_form(self) -> "cat_base.cats.Form":
        for maanim in self.anim.maanims:
            index = anim.bc_anim.AnimType.from_bcu_str(maanim.name)
            if index is None:
                continue
            index_str = io.data.PaddedInt(index.value, 2).to_str()
            maanim.name = f"{self.get_cat_id_str()}_{self.form.value}{index_str}.maanim"
        if len(self.anim.mamodel.ints) == 1:
            self.anim.mamodel.ints.append(self.anim.mamodel.ints[0])
        an = cat_base.cats.Model(self.cat_id, self.form, self.anim)
        return cat_base.cats.Form(
            self.cat_id,
            self.form,
            self.to_stats(),
            self.name,
            self.description,
            an,
            self.upgrade_icon,
            self.deploy_icon,
        )

    def to_stats(self) -> "cat_base.cats.Stats":
        stats = cat_base.cats.Stats(self.cat_id, self.form, [])
        base_stats = self.form_data["du"]
        traits = base_stats["traits"]
        procs = base_stats["rep"]["proc"]
        traits = sorted(traits, key=lambda x: x["id"])
        stats.hp = base_stats["hp"]
        stats.kbs = base_stats["hb"]
        stats.speed.raw = base_stats["speed"]
        stats.attack_1.damage = base_stats["atks"]["pool"][0]["atk"]
        stats.attack_interval = cat_base.unit.Frames(base_stats["tba"])
        stats.range.raw = base_stats["range"]
        stats.cost = base_stats["price"]
        stats.recharge_time = cat_base.unit.Frames(base_stats["resp"])
        stats.collision_width.raw = base_stats["width"]
        stats.target_red = self.get_trait_by_id(traits, 0)
        stats.area_attack = base_stats["atks"]["pool"][0]["range"]
        stats.z_layers.min = base_stats["front"]
        stats.z_layers.max = base_stats["back"]
        stats.target_floating = self.get_trait_by_id(traits, 1)
        stats.target_black = self.get_trait_by_id(traits, 2)
        stats.target_metal = self.get_trait_by_id(traits, 3)
        stats.target_traitless = self.get_trait_by_id(traits, 9)
        stats.target_angel = self.get_trait_by_id(traits, 4)
        stats.target_alien = self.get_trait_by_id(traits, 5)
        stats.target_zombie = self.get_trait_by_id(traits, 6)
        stats.strong = self.check_ability(base_stats["abi"], 0)
        stats.knockback.prob = self.get_proc_prob(procs, "KB")
        stats.freeze.prob = self.get_proc_prob(procs, "STOP")
        stats.freeze.time = self.get_proc_time(procs, "STOP")
        stats.slow.prob = self.get_proc_prob(procs, "SLOW")
        stats.slow.time = self.get_proc_time(procs, "SLOW")
        stats.resistant = self.check_ability(base_stats["abi"], 1)
        stats.insane_damage = self.check_ability(base_stats["abi"], 2)
        stats.crit.prob = self.get_proc_prob(procs, "CRIT")
        stats.attacks_only = self.check_ability(base_stats["abi"], 3)
        stats.extra_money = bool(self.get_proc_mult(procs, "BOUNTY") // 100)
        stats.base_destroyer = bool(self.get_proc_mult(procs, "ATKBASE") // 300)
        stats.wave.is_mini = bool(
            max(
                self.get_proc_prob(procs, "WAVE").percent,
                self.get_proc_prob(procs, "MINIWAVE").percent,
            )
        )
        stats.wave.level = max(
            self.get_proc_level(procs, "WAVE"), self.get_proc_level(procs, "MINIWAVE")
        )
        stats.weaken.prob = self.get_proc_prob(procs, "WEAK")
        stats.weaken.time = self.get_proc_time(procs, "WEAK")
        stats.strengthen.hp_percent = self.get_proc_health(procs, "STRONG")
        stats.strengthen.multiplier_percent = self.get_proc_mult(procs, "STRONG")
        stats.lethal_strike.prob = self.get_proc_prob(procs, "LETHAL")
        stats.is_metal = self.check_ability(base_stats["abi"], 4)
        stats.attack_1.long_distance_start.raw = base_stats["atks"]["pool"][0]["ld0"]
        stats.attack_1.long_distance_range.raw = (
            base_stats["atks"]["pool"][0]["ld1"] - stats.attack_1.long_distance_start
        )
        stats.wave_immunity = bool(self.get_proc_mult(procs, "IMUWAVE"))
        stats.wave_blocker = self.check_ability(base_stats["abi"], 5)
        stats.knockback_immunity = bool(self.get_proc_mult(procs, "IMUKB"))
        stats.freeze_immunity = bool(self.get_proc_mult(procs, "IMUSTOP"))
        stats.slow_immunity = bool(self.get_proc_mult(procs, "IMUSLOW"))
        stats.weaken_immunity = bool(self.get_proc_mult(procs, "IMUWEAK"))
        stats.zombie_killer = self.check_ability(base_stats["abi"], 9)
        stats.witch_killer = self.check_ability(base_stats["abi"], 10)
        stats.target_witch = self.check_ability(base_stats["abi"], 10)
        stats.attack_state.attacks_before = base_stats["loop"]
        stats.attack_state.state_id = (
            2 if self.check_ability(base_stats["abi"], 11) else 0
        )
        stats.attack_2.damage = self.get_attack(base_stats["atks"]["pool"], 1, "atk")
        stats.attack_3.damage = self.get_attack(base_stats["atks"]["pool"], 2, "atk")
        stats.attack_1.foreswing = cat_base.unit.Frames(
            self.get_attack(base_stats["atks"]["pool"], 0, "pre")
        )
        stats.attack_2.foreswing = cat_base.unit.Frames(
            self.get_attack(base_stats["atks"]["pool"], 1, "pre")
        )
        stats.attack_3.foreswing = cat_base.unit.Frames(
            self.get_attack(base_stats["atks"]["pool"], 2, "pre")
        )
        stats.attack_2.use_ability = True
        stats.attack_3.use_ability = True
        stats.soul_anim.model_id = base_stats["death"]["id"]
        stats.barrier_breaker.prob = self.get_proc_prob(procs, "BREAK")
        stats.warp.prob = self.get_proc_prob(procs, "WARP")
        stats.warp.time = self.get_proc_time(procs, "WARP")
        stats.warp.min_distance = self.get_proc_value(procs, "WARP", "dis") * 4
        stats.warp.max_distance = self.get_proc_value(procs, "WARP", "dis") * 4
        stats.warp_blocker = bool(self.get_proc_mult(procs, "IMUWARP"))
        stats.target_eva = self.check_ability(base_stats["abi"], 13)
        stats.eva_killer = self.check_ability(base_stats["abi"], 13)
        stats.target_relic = self.get_trait_by_id(traits, 8)
        stats.curse_immunity = bool(self.get_proc_mult(procs, "IMUCURSE"))
        stats.insanely_tough = self.check_ability(base_stats["abi"], 15)
        stats.insane_damage = self.check_ability(base_stats["abi"], 16)
        stats.savage_blow.prob = self.get_proc_prob(procs, "SATK")
        stats.savage_blow.multiplier = self.get_proc_mult(procs, "SATK")
        stats.dodge.prob = self.get_proc_prob(procs, "IMUATK")
        stats.dodge.time = self.get_proc_time(procs, "IMUATK")
        stats.surge.prob = self.get_proc_prob(procs, "VOLC")
        stats.surge.start.raw = int(self.get_proc_value(procs, "VOLC", "dis_0"))
        stats.surge.range.raw = (
            int(self.get_proc_value(procs, "VOLC", "dis_1")) - stats.surge.start.range
        )
        stats.surge.level = self.get_proc_value(procs, "VOLC", "time") // 20
        stats.toxic_immunity = bool(self.get_proc_mult(procs, "IMUPOIATK"))
        stats.surge_immunity = bool(self.get_proc_mult(procs, "IMUVOLC"))
        stats.curse.prob = self.get_proc_prob(procs, "CURSE")
        stats.curse.time = self.get_proc_time(procs, "CURSE")
        stats.wave.is_mini = self.get_proc_prob(procs, "MINIWAVE").percent != 0
        stats.shield_pierce.prob = self.get_proc_prob(procs, "SHIELDBREAK")
        stats.target_aku = self.get_trait_by_id(traits, 7)
        stats.collossus_slayer = self.check_ability(base_stats["abi"], 17)
        stats.soul_strike = self.check_ability(base_stats["abi"], 18)
        stats.attack_2.long_distance_flag = (
            self.get_attack(base_stats["atks"]["pool"], 1, "ld") != 0
        )
        stats.attack_2.long_distance_start.raw = self.get_attack(
            base_stats["atks"]["pool"], 1, "ld0"
        )
        stats.attack_2.long_distance_range.raw = (
            self.get_attack(base_stats["atks"]["pool"], 1, "ld1")
            - stats.attack_2.long_distance_start.raw
        )
        stats.attack_3.long_distance_flag = (
            self.get_attack(base_stats["atks"]["pool"], 2, "ld") != 0
        )
        stats.attack_3.long_distance_start.raw = self.get_attack(
            base_stats["atks"]["pool"], 2, "ld0"
        )
        stats.attack_3.long_distance_range.raw = (
            self.get_attack(base_stats["atks"]["pool"], 2, "ld1")
            - stats.attack_3.long_distance_start.raw
        )
        stats.behemoth_slayer = self.get_proc_prob(procs, "BSTHUNT").percent != 0
        stats.behemoth_dodge.prob = self.get_proc_prob(procs, "BSTHUNT")
        stats.behemoth_dodge.time = self.get_proc_time(procs, "BSTHUNT")
        stats.attack_1.use_ability = True

        return stats

    @staticmethod
    def get_trait_by_id(traits: list[dict[str, Any]], id: int) -> bool:
        for trait in traits:
            if trait["id"] == id:
                return True
        return False

    @staticmethod
    def check_ability(abi: int, id: int) -> bool:
        has_ability = abi & (1 << id) != 0
        return has_ability

    @staticmethod
    def get_proc_value(procs: dict[str, dict[str, int]], proc_name: str, key: str):
        if proc_name in procs:
            return int(procs[proc_name][key])
        return 0

    @staticmethod
    def get_proc_prob(procs: dict[str, dict[str, int]], proc_name: str):
        return cat_base.unit.Prob(BCUForm.get_proc_value(procs, proc_name, "prob"))

    @staticmethod
    def get_proc_time(procs: dict[str, dict[str, int]], proc_name: str):
        return cat_base.unit.Frames(BCUForm.get_proc_value(procs, proc_name, "time"))

    @staticmethod
    def get_proc_level(procs: dict[str, dict[str, int]], proc_name: str):
        return BCUForm.get_proc_value(procs, proc_name, "lv")

    @staticmethod
    def get_proc_health(procs: dict[str, dict[str, int]], proc_name: str):
        return BCUForm.get_proc_value(procs, proc_name, "health")

    @staticmethod
    def get_proc_mult(procs: dict[str, dict[str, int]], proc_name: str):
        return BCUForm.get_proc_value(procs, proc_name, "mult")

    @staticmethod
    def get_attack(attack_data: list[dict[str, Any]], attack_id: int, key: str):
        try:
            return attack_data[attack_id][key]
        except IndexError:
            return 0


class BCUCat:
    def __init__(
        self,
        unit_data: dict[str, Any],
        anims: list[list["BCUFile"]],
    ):
        self.unit_data = unit_data
        forms = self.unit_data["val"]["forms"]
        self.local_id = self.unit_data["val"]["id"]["id"]
        self.rarity = self.unit_data["val"]["rarity"]
        self.max_base_level = self.unit_data["val"]["max"]
        self.max_plus_level = self.unit_data["val"]["maxp"]
        self.anims = anims
        self.forms: list[BCUForm] = []
        for form_data, form_anims in zip(forms, anims):
            self.forms.append(
                BCUForm(
                    form_data,
                    BCUFileGroup(form_anims),
                )
            )

    def to_cat(
        self,
        unit_buy: "cat_base.cats.UnitBuyData",
        talent: Optional["cat_base.cats.Talent"],
        npbd: "cat_base.cats.NyankoPictureBookData",
        evov_text: list[str],
        cat_id: int,
    ) -> "cat_base.cats.Cat":
        forms: dict[cat_base.cats.FormType, cat_base.cats.Form] = {}
        for form in self.forms:
            forms[form.form] = form.to_cat_form()
        unit_buy.rarity = cat_base.cats.Rarity(self.rarity)
        unit_buy.max_upgrade_level_no_catseye = self.max_base_level
        unit_buy.max_plus_upgrade_level = self.max_plus_level
        unit_buy.max_upgrade_level_catseye = self.max_base_level

        unit = cat_base.cats.Cat(
            cat_id,
            forms,
            unit_buy,
            talent,
            npbd,
            cat_base.cats.EvolveText.create_text_line(evov_text),
        )
        unit.nyanko_picture_book_data.obtainable = True
        unit.unit_buy_data.game_version = (
            0
            if unit.unit_buy_data.game_version == -1
            else unit.unit_buy_data.game_version
        )
        unit.set_cat_id(cat_id)
        return unit

    def get_cat_id(self) -> int:
        for form in self.forms:
            return form.cat_id
        return -1


class BCUEnemy:
    def __init__(self, enemy_data: dict[str, Any], anims: "BCUFileGroup"):
        self.enemy_data = enemy_data
        self.anims = anims
        self.id = self.enemy_data["anim"]["id"]
        self.local_id = self.enemy_data["id"]["id"]
        self.name = self.enemy_data["names"]["dat"][0]["val"]
        self.descritpion = self.enemy_data["description"]["dat"][0]["val"].split("<br>")
        anim = self.load_anim()
        if anim is None:
            return None
        self.anim = anim
        enemy_id = self.get_enemy_id()
        if enemy_id is None:
            enemy_id = -1
        self.enemy_id = enemy_id

    def load_anim(self) -> Optional["anim.bc_anim.Model"]:
        sprite = self.anims.get_file_by_name("sprite.png")
        imgcut = self.anims.get_file_by_name("imgcut.txt")
        mamodel = self.anims.get_file_by_name("mamodel.txt")
        maanims = self.anims.get_files_by_prefix("maanim")
        if sprite is None or imgcut is None or mamodel is None:
            return None
        image = io.bc_image.BCImage(sprite.data)
        imgcut = anim.bc_anim.Imgcut.from_data(imgcut.data, image)
        mamodel = anim.bc_anim.Mamodel.from_data(mamodel.data, imgcut.cuts)
        maanims = [
            anim.bc_anim.Maanim.from_data(maanim.data, maanim.name)
            for maanim in maanims
        ]
        return anim.bc_anim.Model(imgcut, mamodel, maanims)

    def get_enemy_id(self) -> Optional[int]:
        img_name = self.anim.imgcut.image_name
        try:
            enemy_id = int(img_name[:3])
        except ValueError:
            return None
        return enemy_id

    def get_enemy_id_str(self):
        return io.data.PaddedInt(self.enemy_id, 3).to_str()

    def to_enemy(self, enemy_id: int) -> "cat_base.enemies.Enemy":
        for maanim in self.anim.maanims:
            index = anim.bc_anim.AnimType.from_bcu_str(maanim.name)
            if index is None:
                continue
            if index == anim.bc_anim.AnimType.ATTACK:
                maanim.remove_loop_minus_one()
            index_str = io.data.PaddedInt(index.value, 2).to_str()
            maanim.name = f"{self.get_enemy_id_str()}_e{index_str}.maanim"
        an = cat_base.enemies.Model(self.enemy_id, self.anim)
        enemy = cat_base.enemies.Enemy(
            enemy_id,
            self.to_stats(),
            self.name,
            self.descritpion,
            an,
            io.bc_image.BCImage.from_size(64, 64),
        )
        enemy.set_enemy_id(enemy_id)
        return enemy

    def to_stats(self) -> "cat_base.enemies.Stats":
        stats = cat_base.enemies.Stats(self.enemy_id, [])
        base_stats = self.enemy_data["de"]
        traits = base_stats["traits"]
        procs = base_stats["rep"]["proc"]
        traits = sorted(traits, key=lambda x: x["id"])

        stats.hp = base_stats["hp"]
        stats.kbs = base_stats["hb"]
        stats.speed.raw = base_stats["speed"]
        stats.attack_1.damage = base_stats["atks"]["pool"][0]["atk"]
        stats.attack_interval = cat_base.unit.Frames(base_stats["tba"])
        stats.range.raw = base_stats["range"]
        stats.money_drop = base_stats["drop"]
        stats.collision_width.raw = base_stats["width"]
        stats.red = BCUForm.get_trait_by_id(traits, 0)
        stats.area_attack = base_stats["atks"]["pool"][0]["range"]
        stats.floating = BCUForm.get_trait_by_id(traits, 1)
        stats.black = BCUForm.get_trait_by_id(traits, 2)
        stats.metal = BCUForm.get_trait_by_id(traits, 3)
        stats.traitless = BCUForm.get_trait_by_id(traits, 9)
        stats.angel = BCUForm.get_trait_by_id(traits, 4)
        stats.alien = BCUForm.get_trait_by_id(traits, 5)
        stats.zombie = BCUForm.get_trait_by_id(traits, 6)
        stats.knockback.prob = BCUForm.get_proc_prob(procs, "KB")
        stats.freeze.prob = BCUForm.get_proc_prob(procs, "STOP")
        stats.freeze.time = BCUForm.get_proc_time(procs, "STOP")
        stats.slow.prob = BCUForm.get_proc_prob(procs, "SLOW")
        stats.slow.time = BCUForm.get_proc_time(procs, "SLOW")
        stats.crit.prob = BCUForm.get_proc_prob(procs, "CRIT")
        stats.base_destroyer = bool(BCUForm.get_proc_mult(procs, "ATKBASE") // 300)
        stats.wave.is_mini = bool(
            max(
                BCUForm.get_proc_prob(procs, "WAVE").percent,
                BCUForm.get_proc_prob(procs, "MINIWAVE").percent,
            )
        )
        stats.wave.level = max(
            BCUForm.get_proc_level(procs, "WAVE"),
            BCUForm.get_proc_level(procs, "MINIWAVE"),
        )
        stats.weaken.prob = BCUForm.get_proc_prob(procs, "WEAK")
        stats.weaken.time = BCUForm.get_proc_time(procs, "WEAK")
        stats.strengthen.hp_percent = BCUForm.get_proc_health(procs, "STRONG")
        stats.strengthen.multiplier_percent = BCUForm.get_proc_mult(procs, "STRONG")
        stats.survive_lethal_strike.prob = BCUForm.get_proc_prob(procs, "LETHAL")
        stats.attack_1.long_distance_start = base_stats["atks"]["pool"][0]["ld0"]
        stats.attack_1.long_distance_range.raw = (
            base_stats["atks"]["pool"][0]["ld1"]
            - stats.attack_1.long_distance_start.raw
        )
        stats.wave_immunity = bool(BCUForm.get_proc_mult(procs, "IMUWAVE"))
        stats.wave_blocker = BCUForm.check_ability(base_stats["abi"], 5)
        stats.knockback_immunity = bool(BCUForm.get_proc_mult(procs, "IMUKB"))
        stats.freeze_immunity = bool(BCUForm.get_proc_mult(procs, "IMUSTOP"))
        stats.slow_immunity = bool(BCUForm.get_proc_mult(procs, "IMUSLOW"))
        stats.weaken_immunity = bool(BCUForm.get_proc_mult(procs, "IMUWEAK"))
        stats.burrow.count = BCUForm.get_proc_value(procs, "BURROW", "count")
        stats.burrow.distance = BCUForm.get_proc_value(procs, "BURROW", "dis") * 4
        stats.revive.count = BCUForm.get_proc_value(procs, "REVIVE", "count")
        stats.revive.time = BCUForm.get_proc_time(procs, "REVIVE")
        stats.revive.hp_remain_percent = BCUForm.get_proc_health(procs, "REVIVE")
        stats.witch = BCUForm.get_trait_by_id(traits, 10)
        stats.base = BCUForm.get_trait_by_id(traits, 14)
        stats.attack_state.attacks_before = base_stats["loop"]
        stats.attack_state.state_id = (
            2 if BCUForm.check_ability(base_stats["abi"], 11) else 0
        )
        stats.attack_2.damage = BCUForm.get_attack(base_stats["atks"]["pool"], 1, "atk")
        stats.attack_3.damage = BCUForm.get_attack(base_stats["atks"]["pool"], 2, "atk")
        stats.attack_1.foreswing = cat_base.unit.Frames(
            BCUForm.get_attack(base_stats["atks"]["pool"], 0, "pre")
        )
        stats.attack_2.foreswing = cat_base.unit.Frames(
            BCUForm.get_attack(base_stats["atks"]["pool"], 1, "pre")
        )
        stats.attack_3.foreswing = cat_base.unit.Frames(
            BCUForm.get_attack(base_stats["atks"]["pool"], 2, "pre")
        )
        stats.attack_2.use_ability = True
        stats.attack_3.use_ability = True
        stats.soul_anim.model_id = base_stats["death"]["id"]
        stats.barrier.hp = BCUForm.get_proc_health(procs, "BARRIER")
        stats.warp.prob = BCUForm.get_proc_prob(procs, "WARP")
        stats.warp.time = BCUForm.get_proc_time(procs, "WARP")
        stats.warp.min_distance = BCUForm.get_proc_value(procs, "WARP", "dis") * 4
        stats.warp.max_distance = BCUForm.get_proc_value(procs, "WARP", "dis") * 4
        stats.starred_alien = base_stats["star"]
        stats.warp_blocker = bool(BCUForm.get_proc_mult(procs, "IMUWARP"))
        stats.eva_angel = BCUForm.get_trait_by_id(traits, 10)
        stats.relic = BCUForm.get_trait_by_id(traits, 8)
        stats.curse.prob = BCUForm.get_proc_prob(procs, "CURSE")
        stats.curse.time = BCUForm.get_proc_time(procs, "CURSE")
        stats.surge.prob = BCUForm.get_proc_prob(procs, "VOLC")
        stats.savage_blow.prob = BCUForm.get_proc_prob(procs, "SATK")
        stats.savage_blow.multiplier = BCUForm.get_proc_mult(procs, "SATK")
        stats.dodge.prob = BCUForm.get_proc_prob(procs, "IMUATK")
        stats.dodge.time = BCUForm.get_proc_time(procs, "IMUATK")
        stats.toxic.prob = BCUForm.get_proc_prob(procs, "POIATK")
        stats.toxic.hp_percent = BCUForm.get_proc_mult(procs, "POIATK")
        stats.surge.start.raw = int(BCUForm.get_proc_value(procs, "VOLC", "dis_0"))
        stats.surge.range.raw = (
            int(BCUForm.get_proc_value(procs, "VOLC", "dis_1"))
            - stats.surge.start.range
        )
        stats.surge.level = BCUForm.get_proc_value(procs, "VOLC", "time") // 20
        stats.surge_immunity = bool(BCUForm.get_proc_mult(procs, "IMUVOLC"))
        stats.wave.is_mini = BCUForm.get_proc_prob(procs, "MINIWAVE").percent != 0
        stats.shield.hp = BCUForm.get_proc_health(procs, "SHIELD")
        stats.shield.percent_heal_kb = BCUForm.get_proc_value(procs, "SHIELD", "regen")
        stats.death_surge.prob = BCUForm.get_proc_prob(procs, "DEATHSURGE")
        stats.death_surge.start.raw = int(
            BCUForm.get_proc_value(procs, "DEATHSURGE", "dis_0")
        )
        stats.death_surge.range.raw = (
            int(BCUForm.get_proc_value(procs, "DEATHSURGE", "dis_1"))
            - stats.death_surge.start.range
        )
        stats.death_surge.level = (
            BCUForm.get_proc_value(procs, "DEATHSURGE", "time") // 20
        )
        stats.aku = BCUForm.get_trait_by_id(traits, 7)
        stats.baron = BCUForm.get_trait_by_id(traits, 12)
        stats.attack_2.long_distance_flag = (
            BCUForm.get_attack(base_stats["atks"]["pool"], 1, "ld0") != 0
            or BCUForm.get_attack(base_stats["atks"]["pool"], 1, "ld1") != 0
        )
        stats.attack_2.long_distance_start.raw = BCUForm.get_attack(
            base_stats["atks"]["pool"], 1, "ld0"
        )
        stats.attack_2.long_distance_range.raw = (
            BCUForm.get_attack(base_stats["atks"]["pool"], 1, "ld1")
            - stats.attack_2.long_distance_start.raw
        )
        stats.attack_3.long_distance_flag = (
            BCUForm.get_attack(base_stats["atks"]["pool"], 2, "ld0") != 0
            or BCUForm.get_attack(base_stats["atks"]["pool"], 2, "ld1") != 0
        )
        stats.attack_3.long_distance_start.raw = BCUForm.get_attack(
            base_stats["atks"]["pool"], 2, "ld0"
        )
        stats.attack_3.long_distance_range.raw = (
            BCUForm.get_attack(base_stats["atks"]["pool"], 2, "ld1")
            - stats.attack_3.long_distance_start.raw
        )
        stats.behemoth = BCUForm.get_trait_by_id(traits, 13)

        return stats


class BCUFileTypes(enum.Enum):
    ANIMS = "animations"
    MUSIC = "musics"
    PACK = "pack.json"


class BCUFile:
    def __init__(
        self,
        file_info: dict[str, Any],
        enc_data: "io.data.Data",
        key: "io.data.Data",
        iv: "io.data.Data",
    ):
        self.path: str = file_info["path"]
        self.size = file_info["size"]
        self.offset = file_info["offset"]
        self.name = os.path.basename(self.path)
        self.type_str = self.path.split("/")[1]
        self.type = BCUFileTypes(self.type_str)
        self.key = key
        self.iv = iv
        self.padded_size = self.size + (16 - self.size % 16)
        self.enc_data = enc_data[self.offset : self.offset + self.padded_size]
        self.data = self.decrypt()

    def decrypt(self) -> "io.data.Data":
        aes = crypto.AesCipher(self.key.to_bytes(), self.iv.to_bytes())
        data = aes.decrypt(self.enc_data)
        return data[0 : self.size]


class BCUZip:
    def __init__(
        self,
        enc_data: "io.data.Data",
        cc: "country_code.CountryCode",
    ):
        self.enc_data = enc_data
        self.cc = cc
        self.iv, self.key = self.get_iv_key()
        self.json, self.enc_file_data = self.decrypt()
        self.read_json_info()
        self.files = self.load_files()
        pack_json = self.load_pack_json()
        if pack_json is None:
            raise ValueError("Pack json not found")
        self.pack_json = pack_json
        self.cats = self.load_units()
        self.enemies = self.load_enemies()

    @staticmethod
    def from_path(path: "io.path.Path", cc: "country_code.CountryCode") -> "BCUZip":
        return BCUZip(io.data.Data.from_file(path), cc)

    def get_iv_key(self) -> tuple["io.data.Data", "io.data.Data"]:
        iv_str = "battlecatsultimate"
        iv = crypto.Hash(crypto.HashAlgorithm.MD5, io.data.Data(iv_str)).get_hash()
        key = self.enc_data[0x10:0x20]
        return iv, key

    def decrypt(self) -> tuple["io.json_file.JsonFile", "io.data.Data"]:
        json_length = self.enc_data[0x20:0x24].to_int_little()
        json_length_pad = 16 * (json_length // 16 + 1)
        json_data = self.enc_data[0x24 : 0x24 + json_length_pad]
        aes = crypto.AesCipher(self.key.to_bytes(), self.iv.to_bytes())
        json_data = aes.decrypt(json_data)
        json_data = json_data[0:json_length]

        enc_file_data = self.enc_data[0x24 + json_length_pad :]

        json = io.json_file.JsonFile.from_data(json_data)

        return json, enc_file_data

    def read_json_info(self):
        self.desc = self.json["desc"]
        self.files_data = self.json["files"]

        self.bcu_version = self.desc["BCU_VERSION"]
        self.id = self.desc["id"]
        self.author = self.desc["author"]
        self.names = self.desc["names"]
        self.allow_anim = self.desc["allowAnim"]
        self.dependency = self.desc["dependency"]

    def load_files(self) -> list[BCUFile]:
        files: list[BCUFile] = []
        for file_info in self.files_data:
            files.append(BCUFile(file_info, self.enc_file_data, self.key, self.iv))
        return files

    def get_file(self, path: str) -> Optional[BCUFile]:
        for file in self.files:
            if file.path == path:
                return file
        return None

    def get_file_by_name(self, name: str) -> Optional[BCUFile]:
        for file in self.files:
            if file.name == name:
                return file
        return None

    def get_files_by_type(self, type: BCUFileTypes) -> list[BCUFile]:
        files: list[BCUFile] = []
        for file in self.files:
            if file.type == type:
                files.append(file)
        return files

    def get_files_by_dir(self, dir: str) -> list[BCUFile]:
        files: list[BCUFile] = []
        for file in self.files:
            if os.path.basename(os.path.dirname(file.path)) == dir:
                files.append(file)
        return files

    def extract(self, output_dir: "io.path.Path"):
        output_dir = output_dir.add(self.get_name())
        for file in self.files:
            file_path = output_dir.add(file.path)
            file_dir = file_path.parent()
            file_dir.generate_dirs()
            file.data.to_file(file_path)

    def get_name(self) -> str:
        return self.names["dat"][0]["val"]

    def load_pack_json(self) -> Optional["io.json_file.JsonFile"]:
        pack_file = self.get_file_by_name("pack.json")
        if pack_file is None:
            return None
        return io.json_file.JsonFile.from_data(pack_file.data)

    def load_units(self):
        units_data: list[Any] = self.pack_json["units"]["data"]
        units: list[BCUCat] = []
        for unit_data in units_data:
            forms = unit_data["val"]["forms"]
            anims: list[list[BCUFile]] = []
            for form in forms:
                unit_id = form["anim"]["id"]
                anims.append(self.get_files_by_dir(unit_id))
            unit = BCUCat(
                unit_data,
                anims,
            )
            units.append(unit)
        return units

    def load_enemies(self):
        enemies_data: list[Any] = self.pack_json["enemies"]["data"]
        enemies: list[BCUEnemy] = []
        for enemy_data in enemies_data:
            enemy_id = enemy_data["val"]["anim"]["id"]
            anims = self.get_files_by_dir(enemy_id)
            enemy = BCUEnemy(
                enemy_data["val"],
                BCUFileGroup(anims),
            )
            enemies.append(enemy)
        return enemies
