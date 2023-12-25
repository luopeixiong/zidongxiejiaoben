import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox

class FileHandler(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('文件处理器')
        self.setGeometry(100, 100, 400, 400)

        self.queren_msg = QMessageBox()
        self.queren_again()

        self.file_path_label = QLabel('py名:', self)
        self.file_path_label.move(20, 20)

        self.file_path_input = QLineEdit(self)
        self.file_path_input.setGeometry(80, 20, 200, 20)

        self.check_file_button = QPushButton('检查文件', self)
        self.check_file_button.move(300, 20)
        self.check_file_button.clicked.connect(self.check_file)

        self.file_path_label2 = QLabel('全名:', self)
        self.file_path_label2.move(20, 60)

        self.file_path_input2 = QLineEdit(self)
        self.file_path_input2.setGeometry(80, 60, 200, 20)

        self.delete_file_button = QPushButton('删除文件', self)
        self.delete_file_button.move(300, 60)
        self.delete_file_button.clicked.connect(self.delete_file)

        self.log_label = QLabel('操作记录:', self)
        self.log_label.move(20, 100)
        self.log_text = QTextEdit(self)
        self.log_text.setGeometry(20, 130, 350, 250)
        self.log_text.setReadOnly(True)
        self.show()

    def queren_again(self):
        # 创建一个 QMessageBox 对象
        self.queren_msg.setIcon(QMessageBox.Question)
        self.queren_msg.setWindowTitle("再次确认")
        self.queren_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    def check_file(self):
        path = r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishicesi\shishicesi\spiders'
        file_name = self.file_path_input.text()
        meiyou_wenjian = True
        for name in os.listdir(path):
            if file_name in name:
                file_name = os.path.join(path, name)
                os.startfile(file_name)
                self.log_text.append(f'打开文件: {name}')
                meiyou_wenjian = False

        if meiyou_wenjian:
            QMessageBox.warning(self, '警告', '文件不存在！')
            self.log_text.append(f'文件不存在: {file_name}')

    def delete_file(self):
        path = r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishicesi\shishicesi\spiders'
        file_name = self.file_path_input2.text()
        file_path = os.path.join(path, f'{file_name}.py')
        if os.path.isfile(file_path):
            self.queren_msg.setText(f"你确定要删除【{file_name}】吗？")
            # 显示对话框并获取用户的选择
            result = self.queren_msg.exec_()
            if result == QMessageBox.Yes:
                os.remove(file_path)
                QMessageBox.information(self, '提示', '文件已删除！')
                self.log_text.append(f'删除文件: {file_name}')
        else:
            QMessageBox.warning(self, '警告', '文件不存在！')
            self.log_text.append(f'文件不存在: {file_name}')

if __name__ == '__main__':
    app = QApplication([])
    file_handler = FileHandler()
    app.exec_()