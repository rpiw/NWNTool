from PyQt5.QtWidgets import QApplication, QLabel


def install():
    u"""GUI wizard to help with installation and configuration."""
    pass


def main():
    u"""Main window for the entire program."""
    app = QApplication([])
    label = QLabel("NWNTool")  # this should be kept in another file and read from there

    label.show()
    app.exec_()


if __name__ == '__main__':
    main()
