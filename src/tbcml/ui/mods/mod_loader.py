from PyQt5 import QtCore, QtWidgets

from tbcml.core import game_data, io, locale_handler, mods
from tbcml.ui import apk_manager
from tbcml.ui.utils import ui_progress, ui_thread


class ModLoader(QtWidgets.QDialog):
    def __init__(self):
        super(ModLoader, self).__init__()
        self.locale_manager = locale_handler.LocalManager.from_config()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("ModLoader")
        self.resize(400, 300)
        self.setWindowTitle(self.locale_manager.get_key("mod_loader_title"))
        self.setWindowModality(QtCore.Qt.WindowModality.WindowModal)

        self._layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self._layout)

        self.loading_progress_bar = ui_progress.ProgressBar(
            self.locale_manager.get_key("preparing_apk"), None, self
        )
        self._layout.addWidget(self.loading_progress_bar)
        self.loading_progress_bar.show()

        self._data_thread = ui_thread.ThreadWorker.run_in_thread_progress_on_finished(
            self.load_data, ui_thread.ProgressMode.TEXT, self.add_ui
        )
        self._data_thread.progress_text.connect(
            self.loading_progress_bar.set_progress_str
        )

    def load_data(self, progress_signal: QtCore.pyqtSignal):
        progress_signal.emit(  # type: ignore
            self.locale_manager.get_key("getting_selected_apk"), 0, 100
        )
        self.selected_apk = io.config.Config().get(io.config.Key.SELECTED_APK)
        if not self.selected_apk:
            self._layout.addWidget(
                QtWidgets.QLabel(self.locale_manager.get_key("no_apk_selected"))
            )
            self.apk_manager = apk_manager.ApkManager()
            self.apk_manager.show()
            return
        self.apk = io.apk.Apk.from_format_string(self.selected_apk)
        progress_signal.emit(self.locale_manager.get_key("extracting_apk"), 5, 100)  # type: ignore
        self.apk.extract()
        progress_signal.emit(  # type: ignore
            self.locale_manager.get_key("copying_server_files"), 50, 100
        )
        self.apk.copy_server_files()

    def add_ui(self):
        self.loading_progress_bar.close()
        self.loading_mods = False

        self._layout.addWidget(
            QtWidgets.QLabel(
                self.locale_manager.get_key("selected_apk") % self.apk.format()
            )
        )

        self.mod_list = QtWidgets.QListWidget()
        self.mod_list.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self._layout.addWidget(self.mod_list)

        self.load_button = QtWidgets.QPushButton(
            self.locale_manager.get_key("load_selected_mods")
        )
        self.load_button.clicked.connect(self.load_mods)  # type: ignore
        self._layout.addWidget(self.load_button)

        self.load_all_button = QtWidgets.QPushButton(
            self.locale_manager.get_key("load_all_mods")
        )
        self.load_all_button.clicked.connect(self.load_all_mods)  # type: ignore
        self._layout.addWidget(self.load_all_button)

        self.refresh_button = QtWidgets.QPushButton(
            self.locale_manager.get_key("refresh")
        )
        self.refresh_button.clicked.connect(self.refresh_mods)  # type: ignore
        self._layout.addWidget(self.refresh_button)

        self.open_folder_button = QtWidgets.QPushButton(
            self.locale_manager.get_key("reveal_final_apk_folder")
        )
        self.open_folder_button.clicked.connect(self.open_final_apk_folder)
        self._layout.addWidget(self.open_folder_button)

        self.refresh_mods()

    def refresh_mods(self):
        self.mod_list.clear()
        for mod in mods.mod_manager.ModManager().get_mods():
            self.mod_list.addItem(mod.get_full_mod_name())

    def load_mods_wrapper(self, mod_names: list[str]):
        if self.loading_mods:
            return
        self.progress_bar = ui_progress.ProgressBar(
            self.locale_manager.get_key("loading_mods_progress"), None, self
        )
        self._layout.addWidget(self.progress_bar)
        self.progress_bar.show()

        self._thread = ui_thread.ThreadWorker.run_in_thread_progress_on_finished(
            self.load_mods_thread,
            ui_thread.ProgressMode.TEXT,
            self.on_finished,
            mod_names,
        )
        self._thread.progress_text.connect(self.progress_bar.set_progress_str)

    def on_finished(self):
        self.progress_bar.close()
        self.progress_bar.deleteLater()

    def load_mods_thread(
        self, progress_signal: QtCore.pyqtSignal, mod_names: list[str]
    ):
        self.loading_mods = True
        total_progress = 100
        progress_signal.emit(  # type: ignore
            self.locale_manager.get_key("loading_game_data_progress"),
            0,
            total_progress,
        )
        game_packs = game_data.pack.GamePacks.from_apk(self.apk)
        progress_signal.emit(  # type: ignore
            self.locale_manager.get_key("applying_mods_progress"), 10, total_progress
        )
        mds: list[mods.bc_mod.Mod] = []
        for mod_name in mod_names:
            md = mods.mod_manager.ModManager().get_mod_by_full_name(mod_name)
            if md is not None:
                mds.append(md)
        game_packs.apply_mods(mds)
        progress_signal.emit(  # type: ignore
            self.locale_manager.get_key("adding_script_mods_progress"),
            15,
            total_progress,
        )
        self.apk.add_script_mods(mds)
        progress_signal.emit(  # type: ignore
            self.locale_manager.get_key("adding_audio_mods_progress"),
            30,
            total_progress,
        )
        self.apk.add_audio_mods(mds)
        self.apk.load_packs_into_game(game_packs, progress_signal.emit, 35, 100)  # type: ignore

        progress_signal.emit(  # type: ignore
            self.locale_manager.get_key("finished_progress"),
            100,
            total_progress,
        )

        self.loading_mods = False

    def open_final_apk_folder(self):
        path = self.apk.get_final_apk_path()
        if path.exists():
            path.open()
        else:
            path.parent().open()

    def load_mods(self):
        indexes = self.mod_list.selectedIndexes()
        mod_names = [self.mod_list.item(index.row()).text() for index in indexes]
        self.load_mods_wrapper(mod_names)

    def load_all_mods(self):
        mod_names = [
            self.mod_list.item(index).text() for index in range(self.mod_list.count())
        ]
        self.load_mods_wrapper(mod_names)
