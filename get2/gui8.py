import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QHBoxLayout')

        # 创建一个按钮
        addBtn = QPushButton('Add')
        addBtn.clicked.connect(self.addInput)

        # 创建一个布局
        vbox = QVBoxLayout()
        vbox.addWidget(addBtn)

        self.setLayout(vbox)

        self.show()

    def addInput(self):
        # 创建一个水平布局，用于放置输入框和按钮
        hbox = QHBoxLayout()

        # 创建一个输入框
        input = QLineEdit()
        # 获取当前布局中已有的控件数量作为输入框的编号
        count = self.layout().count()
        input.setPlaceholderText('Input {}'.format(count))

        # 添加输入框到水平布局中
        hbox.addWidget(input)

        # 创建一个按钮
        btn = QPushButton('Button {}'.format(count))

        # 添加按钮到水平布局中
        hbox.addWidget(btn)

        # 添加
