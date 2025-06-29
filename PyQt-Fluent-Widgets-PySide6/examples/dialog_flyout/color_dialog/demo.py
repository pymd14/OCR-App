# coding:utf-8
import sys

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import ColorPickerButton, setTheme, Theme


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.button = ColorPickerButton(QColor("#5012aaa2"), '背景色', self, enableAlpha=True)
        self.resize(800, 720)
        self.button.move(500, 500)
        self.setStyleSheet("Demo{background:white}")

        #setTheme(Theme.DARK)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()