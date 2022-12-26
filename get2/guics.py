import sys
from PyQt5.QtWidgets import *
import re
import chuangjian_luoji
import traceback
import json


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.queren_msg = QMessageBox()
        self.queren_again()

        # 创建下拉列表和按键
        self.select = QComboBox()
        self.select.addItems(["0", "_基础数据_", "_start_urlAnddata_", "_start_requests_", "_列表页面_", "_招中标区分_", "_翻页_", "_详细页_"])
        self.select2 = QComboBox()
        self.select2.addItems([])
        self.add_button = QPushButton("Add")
        self.remove_button = QPushButton("Remove")
        self.print_button = QPushButton("Print")
        self.save_button = QPushButton("Save")
        self.load_button = QPushButton("Load")

        self.controls = {}  # 创建控件字典
        self.count = 0  # 记录创建的输入框的数量

        # 设置布局
        layout = QHBoxLayout()
        layout.addWidget(self.select)
        layout.addWidget(self.select2)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.print_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

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
        self.save_button.clicked.connect(self.save_clicked)
        self.load_button.clicked.connect(self.load_clicked)
        self.select.currentIndexChanged[str].connect(self.select_changed)  # 条目发生改变，发射信号，传递条目内容

    def queren_again(self):
        # 创建一个 QMessageBox 对象
        self.queren_msg.setIcon(QMessageBox.Question)
        self.queren_msg.setWindowTitle("再次确认")
        self.queren_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    def load_clicked(self):
        self.queren_msg.setText("你确定要【加载存档】吗？")
        # 显示对话框并获取用户的选择
        result = self.queren_msg.exec_()
        if result == QMessageBox.Yes:
            self.controls = {}
            with open("save.json", "r", encoding="utf-8") as f:
                old_data = json.load(f)
            for k, v in old_data.items():
                dongdai_chuangjian_lst = []
                for _, x in v.items():
                    if x[0] == 'QLineEdit':
                        dongdai_chuangjian_lst.append(QLineEdit(x[1]))
                    elif x[0] == 'QTextEdit':
                        a = QTextEdit()
                        a.setPlainText(x[1])
                        a.setGeometry(55, 20, 200, 20)
                        a.setAcceptRichText(False)
                        dongdai_chuangjian_lst.append(a)
                    elif x[0] == 'QComboBox':
                        if '_start_requests_' in k:
                            a = QComboBox()
                            a.addItems(["_GET_", "_POST_"])
                            dongdai_chuangjian_lst.append(a)

                self.controls[k] = dongdai_chuangjian_lst
            for _, v in self.controls.items():
                for x in v:
                    # 将新创建的控件添加到控件列表和布局中
                    self.scroll_layout.addWidget(x)
        else:
            pass



    def save_clicked(self):
        self.queren_msg.setText("你确定要【保存当前数据】吗？")
        # 显示对话框并获取用户的选择
        result = self.queren_msg.exec_()
        if result == QMessageBox.Yes:
            save_dict = dict()
            for k, v in self.controls.items():
                num = 0
                for x in v:
                    kongjian_leiming = re.findall(r's.(.+?) ', str(x))[0]
                    if num == 0:
                        save_dict[k] = {}
                    save_dict[k][str(num)] = {}
                    if kongjian_leiming == 'QLineEdit':
                        save_dict[k][str(num)] = [kongjian_leiming, x.text()]
                    elif kongjian_leiming == 'QTextEdit':
                        save_dict[k][str(num)] = [kongjian_leiming, x.toPlainText().replace(' ', '\n')]
                    elif kongjian_leiming == 'QComboBox':
                        save_dict[k][str(num)] = [kongjian_leiming, x.currentText()]
                    else:
                        pass
                    num += 1
            with open("save.json", "w", encoding="utf-8") as f:
                json.dump(save_dict, f, ensure_ascii=False, indent=4)
            print('----保存成功------')

    def select_changed(self, i):
        self.select2.clear()
        if "_start_urlAnddata_" in i:
            self.select2.addItems(["_无_", "_查询字符串参数_", "_表单数据_"])
        elif "_列表页面_" in i:
            self.select2.addItems(["_Html格式_", "_Json包_"])
        elif "_招中标区分_" in i:
            self.select2.addItems(["_标题判断_", "_url判断_", "_body判断_"])
        elif "_翻页_" in i:
            self.select2.addItems(["_下一页xpath_", "_url_num增加_", "_正则url_"])
        else:
            pass

    def add_clicked(self):
        # 根据选中的值创建不同的控件
        dongdai_chuangjian_lst = []
        biaoqian = ''
        value = self.select.currentText()
        value2 = self.select2.currentText()
        if "_基础数据_" in value:
            biaoqian = str(self.count) + value + value2
            dongdai_chuangjian_lst.append(QLineEdit("_脚本编号_"))
            dongdai_chuangjian_lst.append(QLineEdit("_脚本中文名_"))
            dongdai_chuangjian_lst.append(QLineEdit("_脚本类名_"))
        elif "_start_urlAnddata_" in value:
            biaoqian = str(self.count) + value + value2
            if '_无_' in value2:
                for x in ["_招标_url_", "_中标_url_"]:
                    a = QTextEdit(x)
                    a.setGeometry(55, 20, 200, 20)
                    a.setAcceptRichText(False)
                    dongdai_chuangjian_lst.append(a)
            elif '_查询字符串参数_' in value2:
                dongdai_chuangjian_lst.append(QLineEdit("_url_"))
                for x in ["_招标_data_", "_中标_data_"]:
                    a = QTextEdit(x)
                    a.setGeometry(55, 20, 200, 20)
                    a.setAcceptRichText(False)
                    dongdai_chuangjian_lst.append(a)
            elif '_表单数据_' in value2:
                dongdai_chuangjian_lst.append(QLineEdit("_url_"))
                for x in ["_招标_data_", "_中标_data_"]:
                    a = QTextEdit(x)
                    a.setGeometry(55, 20, 200, 20)
                    a.setAcceptRichText(False)
                    dongdai_chuangjian_lst.append(a)
        elif "_start_requests_" in value:
            biaoqian = str(self.count) + value + value2
            a = QComboBox()
            a.addItems(["_GET_", "_POST_"])
            dongdai_chuangjian_lst.append(a)
        elif "_列表页面_" in value:
            biaoqian = str(self.count) + value + value2
            if '_Html格式_' in value2:
                dongdai_chuangjian_lst.append(QLineEdit("_标题_xpath_"))
                dongdai_chuangjian_lst.append(QLineEdit("_url_xpath_"))
                dongdai_chuangjian_lst.append(QLineEdit("_时间_xpath_"))
                dongdai_chuangjian_lst.append(QLineEdit(r"(\d\d\d\d\-\d\d\-\d\d)"))
            elif '_Json包_' in value2:
                dongdai_chuangjian_lst.append(QLineEdit("如果值得到详细页的url的id部分，在此写入完整url前段部分"))
        elif "_招中标区分_" in value:
            biaoqian = str(self.count) + value + value2  # "_标题判断_", "_url判断_", "_body判断_"
            if '_标题判断_' in value2:
                dongdai_chuangjian_lst.append(QLineEdit("_招中标区分__标题判断_"))
            elif '_url判断_' in value2:
                dongdai_chuangjian_lst.append(QLineEdit(r"&categorynum=(.+?)&"))
            elif '_url判断_' in value2:
                dongdai_chuangjian_lst.append(QLineEdit("_招中标区分__body判断_"))
        elif "_翻页_" in value:
            biaoqian = str(self.count) + value + value2
            if '_下一页xpath_' in value2:
                dongdai_chuangjian_lst.append(QLineEdit("_下一页xpath_"))
            elif '_url_num增加_' in value2:
                dongdai_chuangjian_lst.append(QLineEdit("把第二页的url后段部分写入，如：index_2.jhtml"))
            elif '_正则url_' in value2:
                dongdai_chuangjian_lst.append(QLineEdit(r"&Paging=(\d+)&【请勿修改\d+】"))
        elif "_详细页_" in value:
            biaoqian = str(self.count) + value + value2
            dongdai_chuangjian_lst.append(QLineEdit("_详细页_标题_xpath_"))
            dongdai_chuangjian_lst.append(QLineEdit("_详细页_时间_xpath_"))
            dongdai_chuangjian_lst.append(QLineEdit(r"(\d\d\d\d\-\d\d\-\d\d)"))
            dongdai_chuangjian_lst.append(QLineEdit("_详细页_正文_xpath_"))
        else:
            pass

        self.controls[biaoqian] = dongdai_chuangjian_lst
        for control in dongdai_chuangjian_lst:
            # 将新创建的控件添加到控件列表和布局中
            self.scroll_layout.addWidget(control)

        self.count += 1
        # print(self.controls)

    def remove_clicked(self):
        self.queren_msg.setText("你确定要【删除最后一个控件组】吗？")
        # 显示对话框并获取用户的选择
        result = self.queren_msg.exec_()
        if result == QMessageBox.Yes:
            # 从控件列表中移除最后一个控件
            if self.controls:
                zuihou_k = ''
                for x in self.controls.keys():
                    zuihou_k = x
                zuihou_v = self.controls[zuihou_k]
                for x in zuihou_v:
                    x.setParent(None)
                del self.controls[zuihou_k]

    def print_clicked(self):
        self.queren_msg.setText("你确定要【创建脚本】吗？")
        # 显示对话框并获取用户的选择
        result = self.queren_msg.exec_()
        if result == QMessageBox.Yes:
            try:
                # 在这里执行你的代码
                chuangjian_luoji.chuangjian(self.controls)
            except Exception as e:
                # 在这里处理所有异常
                QMessageBox.warning(self, "错误", f"发生了一个错误：{traceback.format_exc()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
