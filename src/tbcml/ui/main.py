from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets

from tbcml.core import io, locale_handler, mods
from tbcml.ui import apk_manager, server_files_manager
from tbcml.ui.mods import mod_loader, mod_manager


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(MainWindow, self).__init__(parent)
        self.locale_manager = locale_handler.LocalManager.from_config()
        self.locale_manager.check_duplicates()
        self.asset_manager = io.asset_loader.AssetLoader.from_config()
        mods.mod_manager.ModManager().regenerate_mod_json()
        self.setup_ui()

    def create_toolbar(self):
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setToolButtonStyle(
            QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon
        )
        self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        self.file_menu = QtWidgets.QMenu(self.locale_manager.search_key("file_menu"))
        self.file_menu.addAction(
            self.locale_manager.search_key("apk_manager"), self.open_apk_manager
        )
        self.file_menu.addAction(
            self.locale_manager.search_key("server_files_manager"),
            self.open_server_files_manager,
        )
        self.file_menu.addAction(
            self.locale_manager.search_key("load_mods"), self.load_mods_into_game
        )
        self.toolbar.addAction(self.file_menu.menuAction())

    def setup_ui(self):
        self.asset_manager.load_stylesheet(self)
        self.setObjectName("MainWindow")
        self.resize(900, 700)
        self.create_toolbar()
        self.setWindowTitle(self.locale_manager.search_key("main_title"))
        icon = self.asset_manager.load_icon("icon.png")
        self.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self._layout = QtWidgets.QVBoxLayout()
        self.centralwidget.setLayout(self._layout)

        self.mod_view = mod_manager.ModView(self)
        self._layout.addWidget(self.mod_view)

    def run(self):
        self.show()
        self.raise_()
        self.activateWindow()

        app = QtWidgets.QApplication.instance()
        app.exec_()

    def keyPressEvent(self, event: QtGui.QKeyEvent):  # type: ignore
        if (
            event.key() == QtCore.Qt.Key.Key_C
            and event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier
        ):
            self.close()

    def open_apk_manager(self):
        self.apk_man = apk_manager.ApkManager()
        self.apk_man.show()

    def open_server_files_manager(self):
        self.server_files_manager = server_files_manager.ServerFilesManager()
        self.server_files_manager.show()

    def load_mods_into_game(self):
        self.mod_loader = mod_loader.ModLoader()
        self.mod_loader.show()

    def check_apk_selected(self):
        if not io.config.Config().get(io.config.Key.SELECTED_APK):
            self.open_apk_manager()


def clear_layout(layout: QtWidgets.QLayout):
    while layout.count():
        child = layout.takeAt(0)
        try:
            child.widget().deleteLater()
        except AttributeError:
            pass
        try:
            clear_layout(child.layout())
        except AttributeError:
            pass