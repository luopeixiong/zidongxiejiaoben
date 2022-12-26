import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 创建一个按钮
        btn = QPushButton('点击这里', self)
        btn.clicked.connect(self.showDialog)

        # 设置窗口的布局
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('再次确认对话框')
        self.show()

    def showDialog(self):

        # 创建一个 QMessageBox 对象
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("你确定要继续吗？")
        msg.setWindowTitle("再次确认")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # 显示对话框并获取用户的选择
        result = msg.exec_()

        # 如果用户选择“是”，则执行某些操作
        if result == QMessageBox.Yes:
            print("用户选择了“是”，执行操作。")
        # 否则，执行取消操作
        else:
            print("用户选择了“否”，取消操作。")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
