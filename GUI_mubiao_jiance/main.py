import os
import sys
import time
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QComboBox, QHBoxLayout, QLineEdit, QPushButton, QSpinBox, QToolButton, QVBoxLayout, QWidget
import tkinter as tk

import py_tool
from screenshot import Screenshot


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        jietu_button = QPushButton("截图")
        jietu_button.setFixedWidth(100)
        jietu_button.setFixedHeight(25)

        input_lineedit = QLineEdit()
        input_lineedit.setPlaceholderText("输入坐标,例【333_170@648_351】")
        # 设置宽度和高度
        input_lineedit.setFixedWidth(200)
        input_lineedit.setFixedHeight(25)

        topWidget = QWidget()
        topWidgetLayout = QVBoxLayout(topWidget)
        topWidgetLayout.addWidget(jietu_button)
        topWidgetLayout.addWidget(input_lineedit)
        topWidgetLayout.addStretch(1)
        topWidget.setFixedHeight(200)


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(topWidget)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)
        self.resize(700, 500)


        # 连接信号和槽
        jietu_button.clicked.connect(self.jietu_clicked)

    def jietu_clicked(self):
        scale = py_tool.get_screen_scale_rate()
        py_tool.eliminate_scaling_interference()
        top = tk.Tk()

        Screenshot(top, scale)

        top.mainloop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
