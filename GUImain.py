from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QPushButton, QVBoxLayout, QMainWindow
from PySide2.QtUiTools import QUiLoader
import logging
import session

logger = logging.getLogger(__name__)
gui_session = session.Session()


class MyWidget(QMainWindow):
    u"""Entire gui stuff goes here."""
    def __init__(self):
        super(MyWidget, self).__init__()
        file = QtCore.QFile("mainwindow.ui")
        file.open(QtCore.QFile.ReadOnly)
        self.window = QUiLoader().load(file)
        file.close()


def install():
    u"""GUI wizard to help with installation and configuration."""
    pass


def main():
    u"""Main window for the entire program."""
    app = QApplication([])
    app.setStyle("Fusion")
    widget = MyWidget()
    widget.resize(800, 400)
    widget.window.show()
    app.exec_()


if __name__ == '__main__':
    main()
