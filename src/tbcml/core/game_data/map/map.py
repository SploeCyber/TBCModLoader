import enum
from typing import Any, Optional
from tbcml.core.game_data import pack
from tbcml.core import io


class StageNameNameType(enum.Enum):
    STORY = ""
    AKU = "DM"
    GAUNTLET = "RA"
    DRINK = "RB"
    COLLAB = "RC"
    COLLAB_GAUNTLET = "RCA"
    EXTRA = "RE"
    ENIGMA = "RH"
    CHALLENGE = "RM"
    SOL = "RN"
    UNCANNY = "RNA"
    BEHEMOTH = "RQ"
    DOJO_RANK = "RR"
    REGULAR_EVENT = "RS"
    DOJO_CATCLAW = "RT"
    TOWER = "RV"

    def get_map_index_type(self) -> Optional["MapIndexType"]:
        for index_type in MapIndexType:
            if index_type.name == self.name:
                return index_type
        return None


class MapStageDataNameType(enum.Enum):
    STORY = ""
    SOL = "N"
    REGULAR_EVENT = "S"
    COLLAB = "C"
    EXTRA = "E"
    DOJO_CATCLAW = "T"
    TOWER = "V"
    DOJO_RANK = "R"
    CHALLENGE = "M"
    UNCANNY = "A"
    DRINK = "B"
    GAUNTLET = "RA"
    ENGIMA = "H"
    COLLAB_GAUNTLET = "CA"
    BEHEMOTH = "Q"

    def get_map_index_type(self) -> Optional["MapIndexType"]:
        for index_type in MapIndexType:
            if index_type.name == self.name:
                return index_type
        return None


class MapNameType(enum.Enum):
    STORY = ""
    AKU = "DM"
    EXTRA = "EX"  # also RE
    GAUNTLET = "RA"
    DRINK = "RB"
    COLLAB = "RC"
    COLLAB_GAUNTLET = "RCA"
    ENIGMA = "RH"
    CHALLENGE = "RM"
    SOL = "RN"
    UNCANNY = "RNA"
    BEHEMOTH = "RQ"
    DOJO_RANK = "RR"
    REGULAR_EVENT = "RS"
    DOJO_CATCLAW = "RT"
    TOWER = "RV"
    COTC = "Space"
    ITF = "W"
    OUTBREAKS = "Z"

    def get_map_index_type(self) -> Optional["MapIndexType"]:
        for index_type in MapIndexType:
            if index_type.name == self.name:
                return index_type
        return None


class MapIndexType(enum.Enum):
    SOL = 0
    REGULAR_EVENT = 1000
    COLLAB = 2000
    STORY = 3000
    EXTRA = 4000
    DOJO_CATCLAW = 6000
    TOWER = 7000
    CHALLENGE = 12000
    UNCANNY = 13000
    DRINK = 14000
    LEGEND_QUEST = 16000
    OUTBREAKS_EOC = 20000
    OUTBREAKS_ITF = 21000
    OUTBREAKS_COTC = 22000
    FILIBUSTER = 23000
    GAUNTLET = 24000
    ENGIMA = 25000
    COLLAB_GAUNTLET = 27000
    BEHEMOTH = 31000

    @staticmethod
    def get_all() -> list["MapIndexType"]:
        return sorted(MapIndexType, key=lambda x: x.value)

    def get_map_name_type(self) -> Optional[MapNameType]:
        for name_type in MapNameType:
            if name_type.name == self.name:
                return name_type
        return None

    def get_map_stage_data_name_type(self) -> Optional[MapStageDataNameType]:
        for name_type in MapStageDataNameType:
            if name_type.name == self.name:
                return name_type
        return None

    def get_stage_name_name_type(self) -> Optional[StageNameNameType]:
        for name_type in StageNameNameType:
            if name_type.name == self.name:
                return name_type
        return None

    @staticmethod
    def from_index(index: int) -> Optional["MapIndexType"]:
        types_sorted = sorted(MapIndexType, key=lambda x: x.value)
        for i in range(len(types_sorted)):
            if index < types_sorted[i].value:
                return types_sorted[i - 1]
            if index == types_sorted[i].value:
                return types_sorted[i]
        return None


class ResetType(enum.Enum):
    NONE = 0
    REWARD = 1
    CLEAR_STATUS = 2
    NUMBER_OF_PLAYS = 3


class MapOption:
    def __init__(
        self,
        stage_id: int,
        number_of_stars: int,
        star_mult_1: int,
        star_mult_2: int,
        star_mult_3: int,
        star_mult_4: int,
        guerrilla_set: int,
        reset_type: ResetType,
        one_time_display: bool,
        display_order: int,
        interval: int,
        challenge_flag: bool,
        difficulty_mask: int,
        hide_after_clear: bool,
        map_comment: str,
    ):
        self.stage_id = stage_id
        self.map_index_type = MapIndexType.from_index(stage_id)
        if self.map_index_type is not None:
            self.map_name_type = self.map_index_type.get_map_name_type()
            self.map_stage_data_name_type = (
                self.map_index_type.get_map_stage_data_name_type()
            )

        self.number_of_stars = number_of_stars
        self.star_mult_1 = star_mult_1
        self.star_mult_2 = star_mult_2
        self.star_mult_3 = star_mult_3
        self.star_mult_4 = star_mult_4
        self.guerrilla_set = guerrilla_set
        self.reset_type = reset_type
        self.one_time_display = one_time_display
        self.display_order = display_order
        self.interval = interval
        self.challenge_flag = challenge_flag
        self.difficulty_mask = difficulty_mask
        self.hide_after_clear = hide_after_clear
        self.map_comment = map_comment

    def serialize(self) -> dict[str, Any]:
        return {
            "number_of_stars": self.number_of_stars,
            "star_mult_1": self.star_mult_1,
            "star_mult_2": self.star_mult_2,
            "star_mult_3": self.star_mult_3,
            "star_mult_4": self.star_mult_4,
            "guerrilla_set": self.guerrilla_set,
            "reset_type": self.reset_type.value,
            "one_time_display": self.one_time_display,
            "display_order": self.display_order,
            "interval": self.interval,
            "challenge_flag": self.challenge_flag,
            "difficulty": self.difficulty_mask,
            "hide_after_clear": self.hide_after_clear,
            "map_comment": self.map_comment,
        }

    @staticmethod
    def deserialize(data: dict[str, Any], stage_id: int) -> "MapOption":
        return MapOption(
            stage_id,
            data["number_of_stars"],
            data["star_mult_1"],
            data["star_mult_2"],
            data["star_mult_3"],
            data["star_mult_4"],
            data["guerrilla_set"],
            ResetType(data["reset_type"]),
            data["one_time_display"],
            data["display_order"],
            data["interval"],
            data["challenge_flag"],
            data["difficulty"],
            data["hide_after_clear"],
            data["map_comment"],
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MapOption):
            return False
        return (
            self.stage_id == other.stage_id
            and self.number_of_stars == other.number_of_stars
            and self.star_mult_1 == other.star_mult_1
            and self.star_mult_2 == other.star_mult_2
            and self.star_mult_3 == other.star_mult_3
            and self.star_mult_4 == other.star_mult_4
            and self.guerrilla_set == other.guerrilla_set
            and self.reset_type == other.reset_type
            and self.one_time_display == other.one_time_display
            and self.display_order == other.display_order
            and self.interval == other.interval
            and self.challenge_flag == other.challenge_flag
            and self.difficulty_mask == other.difficulty_mask
            and self.hide_after_clear == other.hide_after_clear
            and self.map_comment == other.map_comment
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class MapOptions:
    def __init__(self, options: dict[int, MapOption]):
        self.options = options

    def serialize(self) -> dict[str, Any]:
        return {
            "options": {str(k): v.serialize() for k, v in self.options.items()},
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "MapOptions":
        return MapOptions(
            {
                int(k): MapOption.deserialize(v, int(k))
                for k, v in data["options"].items()
            }
        )

    def get(self, stage_id: int) -> Optional[MapOption]:
        return self.options.get(stage_id)

    def set(self, option: MapOption):
        self.options[option.stage_id] = option

    @staticmethod
    def get_file_name() -> str:
        return "Map_option.csv"

    @staticmethod
    def from_game_data(game_data: "pack.GamePacks") -> "MapOptions":
        map_options = game_data.find_file(MapOptions.get_file_name())
        if map_options is None:
            return MapOptions.create_empty()
        options: dict[int, MapOption] = {}
        csv = io.bc_csv.CSV(map_options.dec_data)
        for line in csv.lines[1:]:
            stage_id = line[0].to_int()
            options[stage_id] = MapOption(
                stage_id,
                line[1].to_int(),
                line[2].to_int(),
                line[3].to_int(),
                line[4].to_int(),
                line[5].to_int(),
                line[6].to_int(),
                ResetType(line[7].to_int()),
                line[8].to_bool(),
                line[9].to_int(),
                line[10].to_int(),
                line[11].to_bool(),
                line[12].to_int(),
                line[13].to_bool(),
                line[14].to_str(),
            )
        return MapOptions(options)

    def to_game_data(self, game_data: "pack.GamePacks"):
        map_options = game_data.find_file(MapOptions.get_file_name())
        if map_options is None:
            return None
        csv = io.bc_csv.CSV(map_options.dec_data)
        remaining = self.options.copy()
        for i, line in enumerate(csv.lines[1:]):
            stage_id = line[0].to_int()
            option = self.options.get(stage_id)
            if option is None:
                continue
            line[1].set(option.number_of_stars)
            line[2].set(option.star_mult_1)
            line[3].set(option.star_mult_2)
            line[4].set(option.star_mult_3)
            line[5].set(option.star_mult_4)
            line[6].set(option.guerrilla_set)
            line[7].set(option.reset_type.value)
            line[8].set(option.one_time_display)
            line[9].set(option.display_order)
            line[10].set(option.interval)
            line[11].set(option.challenge_flag)
            line[12].set(option.difficulty_mask)
            line[13].set(option.hide_after_clear)
            line[14].set(option.map_comment)
            csv.set_line(i + 1, line)
            del remaining[stage_id]
        for option in remaining.values():
            line: list[Any] = []
            line.append(option.stage_id)
            line.append(option.number_of_stars)
            line.append(option.star_mult_1)
            line.append(option.star_mult_2)
            line.append(option.star_mult_3)
            line.append(option.star_mult_4)
            line.append(option.guerrilla_set)
            line.append(option.reset_type.value)
            line.append(option.one_time_display)
            line.append(option.display_order)
            line.append(option.interval)
            line.append(option.challenge_flag)
            line.append(option.difficulty_mask)
            line.append(option.hide_after_clear)
            line.append(option.map_comment)
            csv.add_line(line)

        game_data.set_file(MapOptions.get_file_name(), csv.to_data())

    @staticmethod
    def create_empty() -> "MapOptions":
        return MapOptions({})

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MapOptions):
            return False
        return self.options == other.options

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class EnemyRow:
    def __init__(
        self,
        index: int,
        enemy_id: int,
        total_spawn_count: int,
        start_frame: int,
        min_spawn_interval: int,
        max_spawn_interval: int,
        spawn_base_percentage: int,
        min_z: int,
        max_z: int,
        boss_flag: bool,
        magnification: int,
        spawn_1: Optional[int] = None,
        castle_1: Optional[int] = None,
        group: Optional[int] = None,
        kill_count: Optional[int] = None,
    ):
        self.index = index
        self.enemy_id = enemy_id
        self.total_spawn_count = total_spawn_count
        self.start_frame = start_frame
        self.min_spawn_interval = min_spawn_interval
        self.max_spawn_interval = max_spawn_interval
        self.spawn_base_percentage = spawn_base_percentage
        self.min_z = min_z
        self.max_z = max_z
        self.boss_flag = boss_flag
        self.magnification = magnification
        self.spawn_1 = spawn_1
        self.castle_1 = castle_1
        self.group = group
        self.kill_count = kill_count

    def serialize(self) -> dict[str, Any]:
        return {
            "enemy_id": self.enemy_id,
            "total_spawn_count": self.total_spawn_count,
            "start_frame": self.start_frame,
            "min_spawn_interval": self.min_spawn_interval,
            "max_spawn_interval": self.max_spawn_interval,
            "spawn_base_percentage": self.spawn_base_percentage,
            "min_z": self.min_z,
            "max_z": self.max_z,
            "boss_flag": self.boss_flag,
            "magnification": self.magnification,
            "spawn_1": self.spawn_1,
            "castle_1": self.castle_1,
            "group": self.group,
            "kill_count": self.kill_count,
        }

    @staticmethod
    def deserialize(data: dict[str, Any], index: int) -> "EnemyRow":
        return EnemyRow(
            index,
            data["enemy_id"],
            data["total_spawn_count"],
            data["start_frame"],
            data["min_spawn_interval"],
            data["max_spawn_interval"],
            data["spawn_base_percentage"],
            data["min_z"],
            data["max_z"],
            data["boss_flag"],
            data["magnification"],
            data.get("spawn_1"),
            data.get("castle_1"),
            data.get("group"),
            data.get("kill_count"),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EnemyRow):
            return False
        return self.serialize() == other.serialize()

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class StageStats:
    def __init__(
        self,
        stage_id: int,
        stage_index: int,
        castle_type: Optional[int],
        no_continues: bool,
        unknowns: list[int],
        stage_width: int,
        base_health: int,
        min_production_frames: int,
        max_production_frames: int,
        background_type: int,
        max_enemy_count: int,
        unused: int,
        enemies: dict[int, EnemyRow],
    ):
        self.stage_id = stage_id
        self.stage_index = stage_index
        self.map_index_type = MapIndexType.from_index(stage_id)
        if self.map_index_type is not None:
            self.map_name_type = self.map_index_type.get_map_name_type()

        self.castle_type = castle_type
        self.no_continues = no_continues
        self.unknowns = unknowns
        self.stage_width = stage_width
        self.base_health = base_health
        self.min_production_frames = min_production_frames
        self.max_production_frames = max_production_frames
        self.background_type = background_type
        self.max_enemy_count = max_enemy_count
        self.unused = unused
        self.enemies = enemies

    @staticmethod
    def get_file_name(stage_id: int, stage_index: int):
        map_index_type = MapIndexType.from_index(stage_id)
        if map_index_type is None:
            return None
        map_name_type = map_index_type.get_map_name_type()
        if map_name_type is None:
            return None
        stage_id_index = stage_id - map_index_type.value
        stage_id_index_str = io.data.PaddedInt(stage_id_index, 3).to_str()
        stage_index_str = io.data.PaddedInt(stage_index, 2).to_str()
        return f"stage{map_name_type.value}{stage_id_index_str}_{stage_index_str}.csv"

    def serialize(self) -> dict[str, Any]:
        return {
            "castle_type": self.castle_type,
            "no_continues": self.no_continues,
            "unknowns": self.unknowns,
            "stage_width": self.stage_width,
            "base_health": self.base_health,
            "min_production_frames": self.min_production_frames,
            "max_production_frames": self.max_production_frames,
            "background_type": self.background_type,
            "max_enemy_count": self.max_enemy_count,
            "unused": self.unused,
            "enemies": {k: v.serialize() for k, v in self.enemies.items()},
        }

    @staticmethod
    def deserialize(
        data: dict[str, Any], stage_id: int, stage_index: int
    ) -> "StageStats":
        return StageStats(
            stage_id,
            stage_index,
            data["castle_type"],
            data["no_continues"],
            data["unknowns"],
            data["stage_width"],
            data["base_health"],
            data["min_production_frames"],
            data["max_production_frames"],
            data["background_type"],
            data["max_enemy_count"],
            data["unused"],
            {
                int(k): EnemyRow.deserialize(v, int(k))
                for k, v in data["enemies"].items()
            },
        )

    @staticmethod
    def from_game_data(
        game_data: "pack.GamePacks", stage_id: int, stage_index: int
    ) -> Optional["StageStats"]:
        file_name = StageStats.get_file_name(stage_id, stage_index)
        if file_name is None:
            return None
        file = game_data.find_file(file_name)
        if file is None:
            return None
        csv = io.bc_csv.CSV(file.dec_data)
        line_1 = csv.read_line()
        if line_1 is None:
            return None
        castle_type = line_1[0].to_int()
        no_continues = line_1[1].to_bool()
        unknowns = io.data.Data.data_list_int_list(line_1[2:])
        line_2 = csv.read_line()
        if line_2 is None:
            return None
        stage_width = line_2[0].to_int()
        base_health = line_2[1].to_int()
        min_production_frames = line_2[2].to_int()
        max_production_frames = line_2[3].to_int()
        background_type = line_2[4].to_int()
        max_enemy_count = line_2[5].to_int()
        unused = line_2[6].to_int()
        enemies: dict[int, EnemyRow] = {}
        for i, line in enumerate(csv.lines[2:]):
            enemy_id = line[0].to_int()
            total_spawn_count = line[1].to_int()
            start_frame = line[2].to_int()
            min_spawn_interval = line[3].to_int()
            max_spawn_interval = line[4].to_int()
            spawn_base_percentage = line[5].to_int()
            min_z = line[6].to_int()
            max_z = line[7].to_int()
            boss_flag = line[8].to_bool()
            magnification = line[9].to_int()
            spawn_1 = None
            castle_1 = None
            group = None
            kill_count = None
            if len(line) > 10:
                spawn_1 = line[10].to_int()
            if len(line) > 11:
                castle_1 = line[11].to_int()
            if len(line) > 12:
                group = line[12].to_int()
            if len(line) > 13:
                kill_count = line[13].to_int()

            enemies[i] = EnemyRow(
                i,
                enemy_id,
                total_spawn_count,
                start_frame,
                min_spawn_interval,
                max_spawn_interval,
                spawn_base_percentage,
                min_z,
                max_z,
                boss_flag,
                magnification,
                spawn_1,
                castle_1,
                group,
                kill_count,
            )
        return StageStats(
            stage_id,
            stage_index,
            castle_type,
            no_continues,
            unknowns,
            stage_width,
            base_health,
            min_production_frames,
            max_production_frames,
            background_type,
            max_enemy_count,
            unused,
            enemies,
        )

    def to_game_data(self, game_data: "pack.GamePacks"):
        file_name = StageStats.get_file_name(self.stage_id, self.stage_index)
        if file_name is None:
            return None
        file = game_data.find_file(file_name)
        if file is None:
            return None
        csv = io.bc_csv.CSV(file.dec_data)
        line_1 = [self.castle_type, self.no_continues, *self.unknowns]
        csv.set_line(0, line_1)
        line_2 = [
            self.stage_width,
            self.base_health,
            self.min_production_frames,
            self.max_production_frames,
            self.background_type,
            self.max_enemy_count,
            self.unused,
        ]
        csv.set_line(1, line_2)
        for i, enemy in self.enemies.items():
            line: list[Any] = [
                enemy.enemy_id,
                enemy.total_spawn_count,
                enemy.start_frame,
                enemy.min_spawn_interval,
                enemy.max_spawn_interval,
                enemy.spawn_base_percentage,
                enemy.min_z,
                enemy.max_z,
                enemy.boss_flag,
                enemy.magnification,
            ]
            if enemy.spawn_1 is not None:
                line.append(enemy.spawn_1)
            if enemy.castle_1 is not None:
                line.append(enemy.castle_1)
            if enemy.group is not None:
                line.append(enemy.group)
            if enemy.kill_count is not None:
                line.append(enemy.kill_count)

            csv.set_line(i + 2, line)
        game_data.set_file(file_name, csv.to_data())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StageStats):
            return False
        return (
            self.stage_id == other.stage_id
            and self.stage_index == other.stage_index
            and self.castle_type == other.castle_type
            and self.no_continues == other.no_continues
            and self.unknowns == other.unknowns
            and self.stage_width == other.stage_width
            and self.base_health == other.base_health
            and self.min_production_frames == other.min_production_frames
            and self.max_production_frames == other.max_production_frames
            and self.background_type == other.background_type
            and self.max_enemy_count == other.max_enemy_count
            and self.unused == other.unused
            and self.enemies == other.enemies
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class Stage:
    def __init__(
        self,
        stage_id: int,
        stage_index: int,
        stage_stats: StageStats,
        name: "StageName",
        name_image: "StageNameImage",
    ):
        self.stage_id = stage_id
        self.stage_index = stage_index
        self.stage_stats = stage_stats
        self.name = name
        self.name_image = name_image

    def serialize(self) -> dict[str, Any]:
        return {
            "stage_stats": self.stage_stats.serialize(),
            "name": self.name.serialize(),
            "name_image": self.name_image.serialize(),
        }

    @staticmethod
    def deserialize(data: dict[str, Any], stage_id: int, stage_index: int) -> "Stage":
        return Stage(
            stage_id,
            stage_index,
            StageStats.deserialize(data["stage_stats"], stage_id, stage_index),
            StageName.deserialize(data["name"], stage_id, stage_index),
            StageNameImage.deserialize(data["name_image"], stage_id, stage_index),
        )

    @staticmethod
    def from_game_data(
        game_data: "pack.GamePacks",
        stage_id: int,
        stage_index: int,
        name: "StageName",
    ) -> Optional["Stage"]:
        stage_stats = StageStats.from_game_data(game_data, stage_id, stage_index)
        stage_image = StageNameImage.from_game_data(game_data, stage_id, stage_index)
        if stage_stats is None or stage_image is None:
            return None
        return Stage(stage_id, stage_index, stage_stats, name, stage_image)

    def to_game_data(self, game_data: "pack.GamePacks"):
        self.stage_stats.to_game_data(game_data)
        self.name_image.to_game_data(game_data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Stage):
            return False
        return (
            self.stage_id == other.stage_id
            and self.stage_index == other.stage_index
            and self.stage_stats == other.stage_stats
            and self.name == other.name
            and self.name_image == other.name_image
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class ItemDrop:
    def __init__(self, probability: int, item_id: int, amount: int):
        self.item_id = item_id
        self.amount = amount
        self.probability = probability

    def serialize(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "amount": self.amount,
            "probability": self.probability,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "ItemDrop":
        return ItemDrop(data["item_id"], data["amount"], data["probability"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ItemDrop):
            return False
        return (
            self.item_id == other.item_id
            and self.amount == other.amount
            and self.probability == other.probability
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"ItemDrop(item_id={self.item_id}, amount={self.amount}, probability={self.probability})"

    def __repr__(self) -> str:
        return self.__str__()


class TimeScoreReward:
    def __init__(self, score: int, item_id: int, amount: int):
        self.score = score
        self.item_id = item_id
        self.amount = amount

    def serialize(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "item_id": self.item_id,
            "amount": self.amount,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "TimeScoreReward":
        return TimeScoreReward(data["score"], data["item_id"], data["amount"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TimeScoreReward):
            return False
        return (
            self.score == other.score
            and self.item_id == other.item_id
            and self.amount == other.amount
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"TimeScoreReward(score={self.score}, item_id={self.item_id}, amount={self.amount})"

    def __repr__(self) -> str:
        return self.__str__()


class MapStageDataStage:
    def __init__(
        self,
        stage_id: int,
        stage_index: int,
        energy_cost: int,
        xp_gain: int,
        start_music: int,
        base_percentage_boss_music: int,
        boss_music: int,
        rand: int,
        item_drops: list[ItemDrop],
        max_reward_claims: int,
        time_score_rewards: list[TimeScoreReward],
    ):
        self.stage_id = stage_id
        self.stage_index = stage_index
        self.energy_cost = energy_cost
        self.xp_gain = xp_gain
        self.start_music = start_music
        self.base_percentage_boss_music = base_percentage_boss_music
        self.boss_music = boss_music
        self.item_drops = item_drops
        self.max_reward_claims = max_reward_claims
        self.time_score_rewards = time_score_rewards
        self.rand = rand

    def serialize(self) -> dict[str, Any]:
        return {
            "energy_cost": self.energy_cost,
            "xp_gain": self.xp_gain,
            "start_music": self.start_music,
            "base_percentage_boss_music": self.base_percentage_boss_music,
            "boss_music": self.boss_music,
            "item_drops": [item_drop.serialize() for item_drop in self.item_drops],
            "max_reward_claims": self.max_reward_claims,
            "time_score_rewards": [
                time_score_reward.serialize()
                for time_score_reward in self.time_score_rewards
            ],
            "rand": self.rand,
        }

    @staticmethod
    def deserialize(
        data: dict[str, Any], stage_id: int, stage_index: int
    ) -> "MapStageDataStage":
        return MapStageDataStage(
            stage_id,
            stage_index,
            data["energy_cost"],
            data["xp_gain"],
            data["start_music"],
            data["base_percentage_boss_music"],
            data["boss_music"],
            data["rand"],
            [ItemDrop.deserialize(item_drop) for item_drop in data["item_drops"]],
            data["max_reward_claims"],
            [
                TimeScoreReward.deserialize(time_score_reward)
                for time_score_reward in data["time_score_rewards"]
            ],
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MapStageDataStage):
            return False
        return (
            self.stage_id == other.stage_id
            and self.stage_index == other.stage_index
            and self.energy_cost == other.energy_cost
            and self.xp_gain == other.xp_gain
            and self.start_music == other.start_music
            and self.base_percentage_boss_music == other.base_percentage_boss_music
            and self.boss_music == other.boss_music
            and self.item_drops == other.item_drops
            and self.max_reward_claims == other.max_reward_claims
            and self.time_score_rewards == other.time_score_rewards
            and self.rand == other.rand
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def clear_item_drops(self):
        self.item_drops = []


class StageNameImage:
    def __init__(
        self,
        stage_id: int,
        stage_index: int,
        image: "io.bc_image.BCImage",
    ):
        self.stage_id = stage_id
        self.stage_index = stage_index
        self.image = image

    def serialize(self) -> dict[str, Any]:
        return {
            "image": self.image.serialize(),
        }

    @staticmethod
    def deserialize(
        data: dict[str, Any], stage_id: int, stage_index: int
    ) -> "StageNameImage":
        return StageNameImage(
            stage_id,
            stage_index,
            io.bc_image.BCImage.deserialize(data["image"]),
        )

    @staticmethod
    def get_file_name(stage_id: int, stage_index: int, lang: str) -> Optional[str]:
        map_index_type = MapIndexType.from_index(stage_id)
        if map_index_type is None:
            return None
        map_stage_data_type = map_index_type.get_map_stage_data_name_type()
        if map_stage_data_type is None:
            return None
        relative_stage_id = stage_id - map_index_type.value
        relative_stage_id_str = io.data.PaddedInt(relative_stage_id, 3).to_str()
        stage_index_str = io.data.PaddedInt(stage_index, 2).to_str()
        return f"mapsn{relative_stage_id_str}_{stage_index_str}_{map_stage_data_type.value.lower()}_{lang}.png"

    @staticmethod
    def from_game_data(
        game_data: "pack.GamePacks",
        stage_id: int,
        stage_index: int,
    ):
        file_name = StageNameImage.get_file_name(
            stage_id, stage_index, game_data.localizable.get_lang()
        )
        if file_name is None:
            return None
        file = game_data.find_file(file_name)
        if file is None:
            return None
        return StageNameImage(
            stage_id,
            stage_index,
            io.bc_image.BCImage(file.dec_data),
        )

    def to_game_data(self, game_data: "pack.GamePacks"):
        file_name = StageNameImage.get_file_name(
            self.stage_id, self.stage_index, game_data.localizable.get_lang()
        )
        if file_name is None:
            return
        game_data.set_file(file_name, self.image.to_data())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StageNameImage):
            return False
        return (
            self.stage_id == other.stage_id
            and self.stage_index == other.stage_index
            and self.image == other.image
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class MapNameImage:
    def __init__(
        self,
        stage_id: int,
        image: "io.bc_image.BCImage",
    ):
        self.stage_id = stage_id
        self.image = image

    def serialize(self) -> dict[str, Any]:
        return {
            "image": self.image.serialize(),
        }

    @staticmethod
    def deserialize(data: dict[str, Any], stage_id: int) -> "MapNameImage":
        return MapNameImage(
            stage_id,
            io.bc_image.BCImage.deserialize(data["image"]),
        )

    @staticmethod
    def get_file_name(stage_id: int, lang: str) -> Optional[str]:
        map_index_type = MapIndexType.from_index(stage_id)
        if map_index_type is None:
            return None
        map_stage_data_type = map_index_type.get_map_stage_data_name_type()
        if map_stage_data_type is None:
            return None
        relative_stage_id = stage_id - map_index_type.value
        relative_stage_id_str = io.data.PaddedInt(relative_stage_id, 3).to_str()
        return f"mapname{relative_stage_id_str}_{map_stage_data_type.value.lower()}_{lang}.png"

    @staticmethod
    def from_game_data(
        game_data: "pack.GamePacks",
        stage_id: int,
    ):
        file_name = MapNameImage.get_file_name(
            stage_id, game_data.localizable.get_lang()
        )
        if file_name is None:
            return None
        file = game_data.find_file(file_name)
        if file is None:
            return None
        return MapNameImage(
            stage_id,
            io.bc_image.BCImage(file.dec_data),
        )

    def to_game_data(self, game_data: "pack.GamePacks"):
        file_name = MapNameImage.get_file_name(
            self.stage_id, game_data.localizable.get_lang()
        )
        if file_name is None:
            return
        game_data.set_file(file_name, self.image.to_data())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MapNameImage):
            return False
        return self.stage_id == other.stage_id and self.image == other.image

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class StageName:
    def __init__(
        self,
        stage_id: int,
        stage_index: int,
        name: str,
    ):
        self.stage_id = stage_id
        self.stage_index = stage_index
        self.name = name

    def serialize(self) -> dict[str, Any]:
        return {
            "name": self.name,
        }

    @staticmethod
    def deserialize(
        data: dict[str, Any], stage_id: int, stage_index: int
    ) -> "StageName":
        return StageName(
            stage_id,
            stage_index,
            data["name"],
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StageName):
            return False
        return (
            self.stage_id == other.stage_id
            and self.stage_index == other.stage_index
            and self.name == other.name
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"StageName({self.stage_id}, {self.stage_index}, {self.name})"


class StageNames:
    def __init__(
        self,
        stage_id: int,
        names: dict[int, StageName],
    ):
        self.stage_id = stage_id
        self.names = names

    def serialize(self) -> dict[str, Any]:
        return {
            "names": {k: v.serialize() for k, v in self.names.items()},
        }

    @staticmethod
    def deserialize(data: dict[str, Any], stage_id: int) -> "StageNames":
        return StageNames(
            stage_id,
            {
                int(k): StageName.deserialize(v, stage_id, int(k))
                for k, v in data["names"].items()
            },
        )

    def get(self, stage_index: int) -> Optional[StageName]:
        return self.names.get(stage_index)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StageNames):
            return False
        return self.stage_id == other.stage_id and self.names == other.names

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"StageNames({self.stage_id}, {self.names})"

    def __repr__(self) -> str:
        return f"StageNames({self.stage_id}, {self.names})"


class StageNameSet:
    def __init__(
        self,
        base_stage_id: int,
        names: dict[int, StageNames],
    ):
        self.base_stage_id = base_stage_id
        map_index_type = MapIndexType.from_index(base_stage_id)
        if map_index_type is None:
            raise ValueError(f"Invalid base stage id {base_stage_id}")
        self.map_index_type = map_index_type
        name_str = self.map_index_type.get_stage_name_name_type()
        if name_str is None:
            name_str = ""
        self.name_str = name_str
        self.names = names

    def serialize(self) -> dict[str, Any]:
        return {
            "names": {k: v.serialize() for k, v in self.names.items()},
        }

    @staticmethod
    def deserialize(data: dict[str, Any], base_stage_id: int) -> "StageNameSet":
        return StageNameSet(
            base_stage_id,
            {
                int(k): StageNames.deserialize(v, int(k))
                for k, v in data["names"].items()
            },
        )

    @staticmethod
    def get_file_name(base_stage_id: int, lang: str):
        map_index_type = MapIndexType.from_index(base_stage_id)
        if map_index_type is None:
            raise ValueError(f"Invalid base stage id {base_stage_id}")
        name_str = map_index_type.get_stage_name_name_type()
        if name_str is None:
            raise ValueError(f"Invalid base stage id {base_stage_id}")
        return f"StageName_{name_str.value}_{lang}.csv"

    @staticmethod
    def from_game_data(
        base_stage_id: int,
        game_data: "pack.GamePacks",
    ) -> "StageNameSet":
        map_index_type = MapIndexType.from_index(base_stage_id)
        if map_index_type is None:
            raise ValueError(f"Invalid base stage id {base_stage_id}")
        name_str = map_index_type.get_stage_name_name_type()
        if name_str is None:
            return StageNameSet.create_empty(base_stage_id)
        file_name = StageNameSet.get_file_name(
            base_stage_id, game_data.localizable.get_lang()
        )
        file = game_data.find_file(file_name)
        if file is None:
            return StageNameSet.create_empty(base_stage_id)
        csv = io.bc_csv.CSV(
            file.dec_data,
            delimeter=io.bc_csv.Delimeter.from_country_code_res(game_data.country_code),
        )
        all_names: dict[int, StageNames] = {}
        for stage_index, line in enumerate(csv.lines):
            stage_id = base_stage_id + stage_index
            names: dict[int, StageName] = {}
            for i, name_str in enumerate(line):
                name = StageName(stage_id, i, name_str.to_str())
                names[name.stage_index] = name
            all_names[stage_id] = StageNames(stage_id, names)

        return StageNameSet(base_stage_id, all_names)

    def to_game_data(
        self,
        game_data: "pack.GamePacks",
    ) -> None:
        file_name = StageNameSet.get_file_name(
            self.base_stage_id, game_data.localizable.get_lang()
        )
        file = game_data.find_file(file_name)
        if file is None:
            raise ValueError(f"Could not find file {file_name}")
        csv = io.bc_csv.CSV(
            file.dec_data,
            delimeter=io.bc_csv.Delimeter.from_country_code_res(game_data.country_code),
            remove_empty=True,
        )
        remaining = self.names.copy()
        for stage_index, line in enumerate(csv.lines):
            stage_id = self.base_stage_id + stage_index
            names = self.names.get(stage_id)
            if names is None:
                continue
            for name_index in range(len(line)):
                name = names.names.get(name_index)
                if name is None:
                    continue
                line[name_index].set(name.name)
            csv.set_line(stage_index, line)
            remaining.pop(stage_id)
        for stage_id, names in remaining.items():
            line = [name.name for name in names.names.values()]
            csv.add_line(line)
        game_data.set_file(file_name, csv.to_data())

    def get(self, stage_id: int) -> Optional[StageNames]:
        return self.names.get(stage_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StageNameSet):
            return False
        return self.base_stage_id == other.base_stage_id and self.names == other.names

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @staticmethod
    def create_empty(base_stage_id: int) -> "StageNameSet":
        return StageNameSet(base_stage_id, {})


class StageNameSets:
    def __init__(
        self,
        sets: dict[MapIndexType, StageNameSet],
    ):
        self.sets = sets

    def serialize(self) -> dict[str, Any]:
        return {
            "sets": {k.value: v.serialize() for k, v in self.sets.items()},
        }

    @staticmethod
    def deserialize(
        data: dict[str, Any],
    ) -> "StageNameSets":
        return StageNameSets(
            {
                MapIndexType(int(k)): StageNameSet.deserialize(v, int(k))
                for k, v in data["sets"].items()
            },
        )

    @staticmethod
    def from_game_data(
        game_data: "pack.GamePacks",
    ) -> "StageNameSets":
        sets: dict[MapIndexType, StageNameSet] = {}
        ids = MapIndexType.get_all()
        for base_stage_id in ids:
            set = StageNameSet.from_game_data(base_stage_id.value, game_data)
            sets[base_stage_id] = set
        return StageNameSets(sets)

    def to_game_data(
        self,
        game_data: "pack.GamePacks",
    ) -> None:
        for set in self.sets.values():
            set.to_game_data(game_data)

    def get(self, stage_id: int) -> Optional[StageNames]:
        map_index_type = MapIndexType.from_index(stage_id)
        if map_index_type is None:
            return None
        set = self.sets.get(map_index_type)
        if set is None:
            return None
        return set.get(stage_id)

    def set(self, stage_id: int, names: StageNames) -> None:
        map_index_type = MapIndexType.from_index(stage_id)
        if map_index_type is None:
            raise ValueError(f"Invalid stage id {stage_id}")
        set = self.sets.get(map_index_type)
        if set is None:
            set = StageNameSet(stage_id, {})
            self.sets[map_index_type] = set
        set.names[stage_id] = names

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StageNameSets):
            return False
        return self.sets == other.sets

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class StageOptionSet:
    def __init__(
        self,
        map_id: int,
        support: int,
        stage_index: int,
        rarity_limit: int,
        deploy_limit: int,
        row_limit: int,
        cost_limit_lower: int,
        cost_limit_upper: int,
        cat_group_id: int,
    ):
        self.map_id = map_id
        self.support = support
        self.stage_index = stage_index
        self.rarity_limit = rarity_limit
        self.deploy_limit = deploy_limit
        self.row_limit = row_limit
        self.cost_limit_lower = cost_limit_lower
        self.cost_limit_upper = cost_limit_upper
        self.cat_group_id = cat_group_id

    def serialize(self) -> dict[str, Any]:
        return {
            "map_id": self.map_id,
            "support": self.support,
            "stage_index": self.stage_index,
            "rarity_limit": self.rarity_limit,
            "deploy_limit": self.deploy_limit,
            "row_limit": self.row_limit,
            "cost_limit_lower": self.cost_limit_lower,
            "cost_limit_upper": self.cost_limit_upper,
            "cat_group_id": self.cat_group_id,
        }

    @staticmethod
    def deserialize(
        data: dict[str, Any],
    ) -> "StageOptionSet":
        return StageOptionSet(
            data["map_id"],
            data["support"],
            data["stage_index"],
            data["rarity_limit"],
            data["deploy_limit"],
            data["row_limit"],
            data["cost_limit_lower"],
            data["cost_limit_upper"],
            data["cat_group_id"],
        )

    @staticmethod
    def from_row(
        row: list[int],
    ) -> "StageOptionSet":
        return StageOptionSet(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            row[8],
        )

    def to_row(self) -> list[int]:
        return [
            self.map_id,
            self.support,
            self.stage_index,
            self.rarity_limit,
            self.deploy_limit,
            self.row_limit,
            self.cost_limit_lower,
            self.cost_limit_upper,
            self.cat_group_id,
        ]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StageOptionSet):
            return False
        return (
            self.map_id == other.map_id
            and self.support == other.support
            and self.stage_index == other.stage_index
            and self.rarity_limit == other.rarity_limit
            and self.deploy_limit == other.deploy_limit
            and self.row_limit == other.row_limit
            and self.cost_limit_lower == other.cost_limit_lower
            and self.cost_limit_upper == other.cost_limit_upper
            and self.cat_group_id == other.cat_group_id
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class StageOption:
    def __init__(
        self,
        sets: dict[int, StageOptionSet],
    ):
        self.sets = sets

    def serialize(self) -> dict[str, Any]:
        return {
            "sets": {k: v.serialize() for k, v in self.sets.items()},
        }

    @staticmethod
    def deserialize(
        data: dict[str, Any],
    ) -> "StageOption":
        return StageOption(
            {int(k): StageOptionSet.deserialize(v) for k, v in data["sets"].items()},
        )

    @staticmethod
    def get_file_name() -> str:
        return "Stage_option.csv"

    @staticmethod
    def from_game_data(game_packs: "pack.GamePacks") -> "StageOption":
        file = game_packs.find_file(StageOption.get_file_name())
        if file is None:
            return StageOption.create_empty()

        csv_file = io.bc_csv.CSV(file.dec_data)
        sets: dict[int, StageOptionSet] = {}
        for line in csv_file.lines:
            set = StageOptionSet.from_row(io.data.Data.data_list_int_list(line))
            sets[set.map_id] = set
        return StageOption(sets)

    def to_game_data(self, game_packs: "pack.GamePacks") -> None:
        file = game_packs.find_file(self.get_file_name())
        if file is None:
            return

        csv_file = io.bc_csv.CSV(file.dec_data)
        remaining = self.sets.copy()
        for i, line in enumerate(csv_file.lines):
            map_id = io.data.Data.data_list_int_list(line)[0]
            if map_id in remaining:
                csv_file.set_line(i, remaining[map_id].to_row())
                del remaining[map_id]
        for set in remaining.values():
            csv_file.add_line(set.to_row())

        game_packs.set_file(self.get_file_name(), csv_file.to_data())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StageOption):
            return False
        return self.sets == other.sets

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def get(self, map_id: int) -> Optional[StageOptionSet]:
        if map_id in self.sets:
            return self.sets[map_id]
        return None

    def set(self, map_id: int, set: StageOptionSet) -> None:
        set.map_id = map_id
        self.sets[map_id] = set

    @staticmethod
    def create_empty() -> "StageOption":
        return StageOption({})


class MapStageData:
    def __init__(
        self,
        stage_id: int,
        map_number: int,
        item_reward_type: int,
        score_reward_type: int,
        unknown_1: int,
        unknown_2: int,
        map_pattern: int,
        data: dict[int, MapStageDataStage],
    ):
        self.stage_id = stage_id
        self.map_number = map_number
        self.item_reward_type = item_reward_type
        self.score_reward_type = score_reward_type
        self.unknown_1 = unknown_1
        self.unknown_2 = unknown_2
        self.map_pattern = map_pattern
        self.data = data

    def serialize(self) -> dict[str, Any]:
        return {
            "map_number": self.map_number,
            "item_reward_type": self.item_reward_type,
            "score_reward_type": self.score_reward_type,
            "unknown_1": self.unknown_1,
            "unknown_2": self.unknown_2,
            "map_pattern": self.map_pattern,
            "data": {k: v.serialize() for k, v in self.data.items()},
        }

    @staticmethod
    def deserialize(data: dict[str, Any], stage_id: int) -> "MapStageData":
        return MapStageData(
            stage_id,
            data["map_number"],
            data["item_reward_type"],
            data["score_reward_type"],
            data["unknown_1"],
            data["unknown_2"],
            data["map_pattern"],
            {
                k: MapStageDataStage.deserialize(v, stage_id, k)
                for k, v in data["data"].items()
            },
        )

    @staticmethod
    def get_file_name(stage_id: int):
        map_index_type = MapIndexType.from_index(stage_id)
        if map_index_type is None:
            return None
        map_type = map_index_type.get_map_stage_data_name_type()
        if map_type is None:
            return None
        stage_index = stage_id - map_index_type.value
        stage_index_str = io.data.PaddedInt(stage_index, 3).to_str()
        return f"MapStageData{map_type.value}_{stage_index_str}.csv"

    @staticmethod
    def from_game_data(
        game_data: "pack.GamePacks", stage_id: int
    ) -> Optional["MapStageData"]:
        file_name = MapStageData.get_file_name(stage_id)
        if file_name is None:
            return None
        file = game_data.find_file(file_name)
        if file is None:
            return None
        csv = io.bc_csv.CSV(file.dec_data)
        data: dict[int, MapStageDataStage] = {}
        line_1 = csv.read_line()
        if line_1 is None:
            return None
        map_number = line_1[0].to_int()
        item_reward_type = line_1[1].to_int()
        score_reward_type = line_1[2].to_int()
        unknown_1 = line_1[3].to_int()
        unknown_2 = line_1[4].to_int()

        line_2 = csv.read_line()
        if line_2 is None:
            return None
        map_pattern = line_2[0].to_int()

        for stage_index, line in enumerate(csv.lines[2:]):
            energy = line[0].to_int()
            xp = line[1].to_int()
            mus_id0 = line[2].to_int()
            mus_hp = line[3].to_int()
            mus_id1 = line[4].to_int()
            reward_once = line[-1].to_int()
            is_time = len(line) > 15
            time: list[TimeScoreReward] = []
            item_drops: list[ItemDrop] = []
            rand = 0

            if is_time:
                for i in range(8, 15):
                    if line[i].to_int() != -2:
                        is_time = False
                        break
            if is_time:
                length = (len(line) - 17) // 3
                for i in range(length):
                    time.append(
                        TimeScoreReward(
                            line[16 + i * 3].to_int(),
                            line[17 + i * 3].to_int(),
                            line[18 + i * 3].to_int(),
                        )
                    )
            is_multi = (not is_time) and len(line) > 9
            if is_multi:
                rand = line[8].to_int()
                drop_length = (len(line) - 7) // 3
                for i in range(0, drop_length):
                    item_drops.append(
                        ItemDrop(
                            line[6 + i * 3].to_int(),
                            line[7 + i * 3].to_int(),
                            line[8 + i * 3].to_int(),
                        )
                    )
            if (len(item_drops) > 0) or not is_multi:
                if len(item_drops) == 0:
                    item_drops.append(
                        ItemDrop(line[5].to_int(), line[6].to_int(), line[7].to_int())
                    )
                else:
                    item_drops[0] = ItemDrop(
                        line[5].to_int(), line[6].to_int(), line[7].to_int()
                    )
            data[stage_index] = MapStageDataStage(
                stage_id,
                stage_index,
                energy,
                xp,
                mus_id0,
                mus_hp,
                mus_id1,
                rand,
                item_drops,
                reward_once,
                time,
            )
        return MapStageData(
            stage_id,
            map_number,
            item_reward_type,
            score_reward_type,
            unknown_1,
            unknown_2,
            map_pattern,
            data,
        )

    def to_game_data(self, game_data: "pack.GamePacks") -> None:
        file_name = MapStageData.get_file_name(self.stage_id)
        if file_name is None:
            return None
        file = game_data.find_file(file_name)
        if file is None:
            return None
        csv = io.bc_csv.CSV(file.dec_data)
        line_1: list[int] = [
            self.map_number,
            self.item_reward_type,
            self.score_reward_type,
            self.unknown_1,
            self.unknown_2,
        ]
        csv.set_line(0, line_1)
        line_2: list[int] = [self.map_pattern]
        csv.set_line(1, line_2)
        for i, stage in self.data.items():
            line: list[int] = [
                stage.energy_cost,
                stage.xp_gain,
                stage.start_music,
                stage.base_percentage_boss_music,
                stage.boss_music,
            ]
            if len(stage.item_drops) > 0:
                line.append(stage.item_drops[0].probability)
                line.append(stage.item_drops[0].item_id)
                line.append(stage.item_drops[0].amount)
            else:
                line.append(0)
                line.append(0)
                line.append(0)
            if len(stage.item_drops) > 1:
                line.append(stage.rand)
            if len(stage.item_drops) > 1:
                for drop in stage.item_drops[1:]:
                    line.append(drop.probability)
                    line.append(drop.item_id)
                    line.append(drop.amount)
            if stage.time_score_rewards:
                line[8:15] = [-2] * 7
                line.append(1)
            for time in stage.time_score_rewards:
                line.append(time.score)
                line.append(time.item_id)
                line.append(time.amount)
            line.append(stage.max_reward_claims)
            csv.set_line(i + 2, line)

        game_data.set_file(file_name, csv.to_data())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MapStageData):
            return False
        return (
            self.map_number == other.map_number
            and self.item_reward_type == other.item_reward_type
            and self.score_reward_type == other.score_reward_type
            and self.unknown_1 == other.unknown_1
            and self.unknown_2 == other.unknown_2
            and self.map_pattern == other.map_pattern
            and self.data == other.data
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class Map:
    def __init__(
        self,
        stage_id: int,
        map_option: MapOption,
        map_stage_data: MapStageData,
        stages: dict[int, "Stage"],
        map_name_image: MapNameImage,
        restriction: Optional[StageOptionSet] = None,
    ):
        self.stage_id = stage_id
        self.map_option = map_option
        self.map_stage_data = map_stage_data
        self.stages = stages
        self.map_name_image = map_name_image
        self.restriction = restriction

    def serialize(self) -> dict[str, Any]:
        return {
            "map_option": self.map_option.serialize(),
            "map_stage_data": self.map_stage_data.serialize(),
            "stages": {k: v.serialize() for k, v in self.stages.items()},
            "map_name_image": self.map_name_image.serialize(),
            "restriction": self.restriction.serialize() if self.restriction else None,
        }

    @staticmethod
    def deserialize(data: dict[str, Any], stage_id: int) -> "Map":
        return Map(
            stage_id,
            MapOption.deserialize(data["map_option"], stage_id),
            MapStageData.deserialize(data["map_stage_data"], stage_id),
            {k: Stage.deserialize(v, stage_id, k) for k, v in data["stages"].items()},
            MapNameImage.deserialize(data["map_name_image"], stage_id),
            StageOptionSet.deserialize(data["restriction"])
            if data["restriction"]
            else None,
        )

    @staticmethod
    def from_game_data(
        game_data: "pack.GamePacks",
        stage_id: int,
        map_options: MapOptions,
        stage_names: StageNames,
        stage_options: StageOption,
    ) -> Optional["Map"]:
        map_option = map_options.get(stage_id)
        map_stage_data = MapStageData.from_game_data(game_data, stage_id)
        map_name_image = MapNameImage.from_game_data(game_data, stage_id)
        restriction = stage_options.get(stage_id)
        i = 0
        stages: dict[int, Stage] = {}
        while True:
            stage_name = stage_names.get(i)
            if stage_name is None:
                break
            stage = Stage.from_game_data(game_data, stage_id, i, stage_name)
            if stage is None:
                break
            stages[i] = stage
            i += 1
        if map_option is None or map_stage_data is None or map_name_image is None:
            return None

        return Map(
            stage_id, map_option, map_stage_data, stages, map_name_image, restriction
        )

    def to_game_data(self, game_data: "pack.GamePacks"):
        self.map_stage_data.to_game_data(game_data)
        self.map_name_image.to_game_data(game_data)
        for stage in self.stages.values():
            stage.to_game_data(game_data)

    def get_names(self) -> StageNames:
        return StageNames(self.stage_id, {k: v.name for k, v in self.stages.items()})

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Map):
            return False
        return (
            self.stage_id == other.stage_id
            and self.map_option == other.map_option
            and self.map_stage_data == other.map_stage_data
            and self.stages == other.stages
            and self.map_name_image == other.map_name_image
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class Maps:
    def __init__(self, maps: dict[int, Map]):
        self.maps = maps

    def serialize(self) -> dict[str, Any]:
        return {
            "maps": {str(k): v.serialize() for k, v in self.maps.items()},
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "Maps":
        return Maps(
            {int(k): Map.deserialize(v, int(k)) for k, v in data["maps"].items()}
        )

    def get(self, stage_id: int) -> Optional[Map]:
        return self.maps.get(stage_id)

    def set(self, map: Map):
        self.maps[map.map_option.stage_id] = map

    @staticmethod
    def from_game_data(game_data: "pack.GamePacks"):
        map_options = MapOptions.from_game_data(game_data)
        stage_name_sets = StageNameSets.from_game_data(game_data)
        stage_options = StageOption.from_game_data(game_data)
        maps: dict[int, Map] = {}
        stage_id = 0
        while stage_id < 100000:
            stage_names = stage_name_sets.get(stage_id)
            if stage_names is None:
                stage_id += 1
                continue
            map = Map.from_game_data(
                game_data, stage_id, map_options, stage_names, stage_options
            )
            if map is None:
                stage_id += 1
                continue
            maps[stage_id] = map
            stage_id += 1
        return Maps(maps)

    def to_game_data(self, game_data: "pack.GamePacks"):
        map_options = MapOptions({})
        stage_name_sets = StageNameSets({})
        stage_options = StageOption({})
        for map in self.maps.values():
            map.to_game_data(game_data)
            map_options.set(map.map_option)
            stage_name_sets.set(map.map_option.stage_id, map.get_names())
            if map.restriction is not None:
                stage_options.set(map.restriction.map_id, map.restriction)

        map_options.to_game_data(game_data)
        stage_name_sets.to_game_data(game_data)
        stage_options.to_game_data(game_data)

    @staticmethod
    def get_maps_json_file_name() -> "io.path.Path":
        return io.path.Path("maps").add("maps.json")

    def add_to_zip(self, zip: "io.zip.Zip"):
        json = io.json_file.JsonFile.from_object(self.serialize())
        zip.add_file(Maps.get_maps_json_file_name(), json.to_data())

    @staticmethod
    def from_zip(zip: "io.zip.Zip") -> "Maps":
        json = zip.get_file(Maps.get_maps_json_file_name())
        if json is None:
            return Maps.create_empty()
        return Maps.deserialize(io.json_file.JsonFile.from_data(json).get_json())

    @staticmethod
    def create_empty() -> "Maps":
        return Maps({})

    def set_map(self, map: Map):
        self.maps[map.map_option.stage_id] = map

    def import_maps(self, other: "Maps", game_data: "pack.GamePacks"):
        """_summary_

        Args:
            other (Maps): _description_
            game_data (pack.GamePacks): The game data to check if the imported data is different from the game data. This is used to prevent overwriting the current data with base game data.
        """
        gd_maps = Maps.from_game_data(game_data)
        all_keys = set(gd_maps.maps.keys())
        all_keys.update(other.maps.keys())
        all_keys.update(self.maps.keys())
        for id in all_keys:
            gd_map = gd_maps.get(id)
            other_map = other.get(id)
            if other_map is None:
                continue
            if gd_map is not None:
                if gd_map != other_map:
                    self.maps[id] = other_map
            else:
                self.maps[id] = other_map