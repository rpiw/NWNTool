from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide2 import QtGui
from mainwindow import Ui_MainWindow
import logging
import session


logger = logging.getLogger(__name__)
gui_session = session.Session()


class MainWindow(QMainWindow):
    u"""Entire gui stuff goes here."""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_1.clicked.connect(lambda name: self.get_directory_name(self.ui.lineEdit_1))  # Diamond Edition Exe
        self.ui.pushButton_2.clicked.connect(lambda name: self.get_directory_name(self.ui.lineEdit_2))  # Local directory for diamond
        self.ui.pushButton_3.clicked.connect(lambda name: self.get_directory_name(self.ui.lineEdit_3))  # EE exe
        self.ui.pushButton_4.clicked.connect(lambda name: self.get_directory_name(self.ui.lineEdit_4))  # Local directory for EE
        self.ui.pushButton_5.clicked.connect(lambda name: self.get_directory_name(self.ui.lineEdit_5))  # NWNTool dir

    def get_directory_name(self, placeholder):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        path = dialog.getExistingDirectory(self, "Select Directory")
        placeholder.setText(path)
        logger.debug(f"Set Text {path} for {placeholder}")


def install():
    u"""GUI wizard to help with installation and configuration."""
    pass


def main():
    u"""Main window for the entire program."""
    app = QApplication([])
    app.setStyle("Fusion")
    widget = MainWindow()
    widget.show()
    app.exec_()


if __name__ == '__main__':
    main()
