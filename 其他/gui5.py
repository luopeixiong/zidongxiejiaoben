import sys
from PyQt5.QtWidgets import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建下拉列表和按键
        self.select = QComboBox()
        self.select.addItems(["0", "1", "2"])
        self.add_button = QPushButton("Add")
        self.remove_button = QPushButton("Remove")
        self.print_button = QPushButton("Print")

        # 创建一个控件列表，用于存储输入框和按键
        self.controls = []

        # 设置布局
        layout = QHBoxLayout()
        layout.addWidget(self.select)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.print_button)

        # 在布局的底部添加一个垂直滚动条，用于滚动控件列表
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        scroll.setWidget(self.scroll_content)
        layout.addWidget(scroll)

        # 设置布局
        self.setLayout(layout)

        # 连接信号和槽
        self.add_button.clicked.connect(self.add_clicked)
        self.remove_button.clicked.connect(self.remove_clicked)
        self.print_button.clicked.connect(self.print_clicked)

    def add_clicked(self):
        # 根据选中的值创建不同的控件
        value = self.select.currentText()
        if value == "1":
            control = QLineEdit()
        elif value == "2":
            control = QPushButton("Button")
        else:
            return

        # 将新创建的控件添加到控件列表和布局中
        self.controls.append(control)
        self.scroll_layout.addWidget(control)

    def remove_clicked(self):
        # 从控件列表中移除最后一个控件
        if self.controls:
            control = self.controls.pop()
            control.setParent(None)

    def print_clicked(self):
        print(self.controls)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
