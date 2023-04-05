import os
import sys
from PyQt5.QtWidgets import *
import re
import chuangjian_luoji
import traceback
import json
import natsort


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.insert_button = None
        self.remove2_button = None

        self.zuixin_hobby_box2 = None

        self.resize(700, 500)

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
        self.controls2 = {}  # 创建控件字典
        self.count = 0  # 记录创建的输入框的数量

        # 设置布局
        layout = QHBoxLayout()
        layout2 = QVBoxLayout()
        self.layout3 = QVBoxLayout()

        layout2.addWidget(self.select)
        layout2.addWidget(self.select2)
        layout2.addWidget(self.add_button)
        layout2.addWidget(self.remove_button)
        layout2.addWidget(self.print_button)
        layout2.addWidget(self.save_button)
        layout2.addWidget(self.load_button)

        # 在布局的底部添加一个垂直滚动条，用于滚动控件列表
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        scroll.setWidget(self.scroll_content)
        self.layout3.addWidget(scroll)

        # 设置布局
        layout.addLayout(layout2)
        layout.addLayout(self.layout3)
        self.setLayout(layout)

        # 连接信号和槽
        self.add_button.clicked.connect(self.add_clicked)
        self.remove_button.clicked.connect(self.remove_clicked)
        self.print_button.clicked.connect(self.print_clicked)
        self.save_button.clicked.connect(self.save_clicked)
        self.load_button.clicked.connect(self.load_clicked)
        self.select.currentIndexChanged[str].connect(self.select_changed)  # 条目发生改变，发射信号，传递条目内容

    def replace_kongjianzu(self):
        self.queren_msg.setText("你确定要【在此控件组上替换新控件组】吗？")
        # 显示对话框并获取用户的选择
        result = self.queren_msg.exec_()
        if result == QMessageBox.Yes:
            self.add_kongjianzu()
            zuihou_k = ''
            button = self.sender()
            button_name = button.objectName()
            button_name = button_name.split('#')[0]
            for x in self.controls2.keys():
                if button_name in x:
                    zuihou_k = x
                    break
            qg_zuihou_v = self.controls2[zuihou_k]
            dangqian_kongjianzu = self.scroll_layout.indexOf(qg_zuihou_v)  # self.scroll_layout
            self.scroll_layout.insertWidget(dangqian_kongjianzu, self.zuixin_hobby_box2)
            qg_zuihou_v.setParent(None)

            del self.controls[zuihou_k]
            del self.controls2[zuihou_k]

    def remove_clicked2(self):
        self.queren_msg.setText("你确定要【删除当前控件组】吗？")
        # 显示对话框并获取用户的选择
        result = self.queren_msg.exec_()
        if result == QMessageBox.Yes:
            # 从控件列表中移除最后一个控件
            if self.controls2:
                zuihou_k = ''
                button = self.sender()
                button_name = button.objectName()
                button_name = button_name.split('#')[0]
                for x in self.controls2.keys():
                    if button_name in x:
                        zuihou_k = x
                        break
                qg_zuihou_v = self.controls2[zuihou_k]
                qg_zuihou_v.setParent(None)

                del self.controls[zuihou_k]
                del self.controls2[zuihou_k]

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
        elif "_列表页面_" in i or "_详细页_" in i:
            self.select2.addItems(["_Html格式_", "_Json包_"])
        elif "_招中标区分_" in i:
            self.select2.addItems(["_标题判断_", "_url判断_", "_body判断_"])
        elif "_翻页_" in i:
            self.select2.addItems(["_下一页xpath_", "_url_num增加_", "_正则url_", "_正则body_"])
        else:
            pass

    def add_kongjianzu(self):
        # 根据选中的值创建不同的控件
        hobby_box2 = QGroupBox('')
        layout4 = QHBoxLayout()
        dongdai_chuangjian_lst = []
        value = self.select.currentText()
        value2 = self.select2.currentText()
        biaoqian = '@' + str(self.count) + '_' + value + value2
        hobby_box = QGroupBox('')
        from_layout = QFormLayout()
        if "_基础数据_" in value:
            hobby_box = QGroupBox(value + value2)
            for x in ['脚本编号', '脚本中文名', '脚本类名', '请求标头Content-Type']:
                lb = QLabel(x)
                le = QLineEdit("")
                dongdai_chuangjian_lst.append(le)
                from_layout.addRow(lb, le)
            hobby_box.setLayout(from_layout)
        elif "_start_urlAnddata_" in value:
            hobby_box = QGroupBox(value + value2)
            if '_无_' in value2 or '_查询字符串参数_' in value2:
                for x in ["_招标_url_", "_中标_url_"]:
                    a = QTextEdit()
                    a.setGeometry(55, 20, 200, 20)
                    a.setAcceptRichText(False)
                    dongdai_chuangjian_lst.append(a)
                    from_layout.addRow(x, a)
                hobby_box.setLayout(from_layout)
            elif '_表单数据_' in value2:
                le = QLineEdit()
                dongdai_chuangjian_lst.append(le)
                from_layout.addRow('_url_', le)
                for x in ["_招标_data_", "_中标_data_"]:
                    a = QTextEdit(x)
                    a.setGeometry(55, 20, 200, 20)
                    a.setAcceptRichText(False)
                    dongdai_chuangjian_lst.append(a)
                    from_layout.addRow(x, a)
                hobby_box.setLayout(from_layout)
        elif "_start_requests_" in value:
            hobby_box = QGroupBox(value + value2)
            a = QComboBox()
            a.addItems(["_GET_", "_POST_"])
            dongdai_chuangjian_lst.append(a)
            from_layout.addRow('start_requests', a)
            hobby_box.setLayout(from_layout)
        elif "_列表页面_" in value:
            hobby_box = QGroupBox(value + value2)
            if '_Html格式_' in value2:
                for x in ['标题_xpath', 'url_xpath', '时间_xpath']:
                    le = QLineEdit()
                    dongdai_chuangjian_lst.append(le)
                    from_layout.addRow(x, le)
                    hobby_box.setLayout(from_layout)
                le = QLineEdit(r"(\d\d\d\d\-\d\d\-\d\d)")
                dongdai_chuangjian_lst.append(le)
                from_layout.addRow('时间re', le)
                hobby_box.setLayout(from_layout)
            elif '_Json包_' in value2:
                for x in ['url_pinjie_qianduan', '列表定位', '列表标题定位', '列表url定位', '列表时间定位']:
                    le = QLineEdit()
                    dongdai_chuangjian_lst.append(le)
                    from_layout.addRow(x, le)
                    hobby_box.setLayout(from_layout)
                le = QLineEdit(r"(\d\d\d\d\-\d\d\-\d\d)")
                dongdai_chuangjian_lst.append(le)
                from_layout.addRow('时间re', le)
                hobby_box.setLayout(from_layout)
        elif "_招中标区分_" in value:
            hobby_box = QGroupBox(value + value2)
            le = QLineEdit()
            if '_标题判断_' in value2:
                le.setText("结果,中选,成交,中标,废标,流标")
                dongdai_chuangjian_lst.append(le)
                from_layout.addRow(value2, le)
                hobby_box.setLayout(from_layout)
            elif '_url判断_' in value2:
                le.setText(r"&categorynum=(.+?)&")
                dongdai_chuangjian_lst.append(le)
                from_layout.addRow(value2, le)
                hobby_box.setLayout(from_layout)
            elif '_body判断_' in value2:
                le.setText(r'"announcement":"(.+?)"')
                dongdai_chuangjian_lst.append(le)
                from_layout.addRow(value2, le)
                hobby_box.setLayout(from_layout)
        elif "_翻页_" in value:
            hobby_box = QGroupBox(value + value2)
            if '_下一页xpath_' in value2:
                le = QLineEdit()
                le.setText('//a[contains(text(), "下页")]/@href')
                dongdai_chuangjian_lst.append(le)
                from_layout.addRow(value2, le)
            elif '_url_num增加_' in value2:
                le = QLineEdit()
                le.setText("index_2.jhtml")
                dongdai_chuangjian_lst.append(le)
                from_layout.addRow(value2, le)
            elif '_正则url_' in value2:
                dic = {'url_Re': r"&Paging=(\d+)&【请勿修改\d+】", 'url_num_add': r"30【增加的数组】"}
                for k, v in dic.items():
                    le = QLineEdit()
                    le.setText(v)
                    dongdai_chuangjian_lst.append(le)
                    from_layout.addRow(k, le)
            elif '_正则body_' in value2:
                dic = {'body_Re': r'pageNum":(\d+)&【请勿修改\d+】', 'body_num_add': r'30【增加的数组】'}
                for k, v in dic.items():
                    le = QLineEdit()
                    le.setText(v)
                    dongdai_chuangjian_lst.append(le)
                    from_layout.addRow(k, le)
            hobby_box.setLayout(from_layout)
        elif "_详细页_" in value:
            hobby_box = QGroupBox(value + value2)
            if '_Html格式_' in value2:
                dic = {'详细页_标题_xpath': '', '详细页_时间_xpath': '', '详细页_时间_re': r"(\d\d\d\d\-\d\d\-\d\d)", '详细页_正文_xpath': ""}
                for k, v in dic.items():
                    le = QLineEdit()
                    le.setText(v)
                    dongdai_chuangjian_lst.append(le)
                    from_layout.addRow(k, le)
            elif '_Json包_' in value2:
                dic = {'详细页title定位': '【逗号做分隔符,记得是全路径】', '详细页正文定位': '【逗号做分隔符,记得是全路径】', '详细页time定位': r"【逗号做分隔符,记得是全路径】", '详细页timeRe': r"(\d\d\d\d\-\d\d\-\d\d)"}
                for k, v in dic.items():
                    le = QLineEdit()
                    le.setText(v)
                    dongdai_chuangjian_lst.append(le)
                    from_layout.addRow(k, le)
            hobby_box.setLayout(from_layout)
        else:
            pass
        self.remove2_button = QPushButton("Remove")
        self.remove2_button.setObjectName('@{}_#remove2'.format(str(self.count)))
        self.remove2_button.clicked.connect(self.remove_clicked2)

        self.insert_button = QPushButton("replace")
        self.insert_button.setObjectName('@{}_#replace'.format(str(self.count)))
        self.insert_button.clicked.connect(self.replace_kongjianzu)

        layout5 = QVBoxLayout()
        layout5.addWidget(self.remove2_button)
        layout5.addWidget(self.insert_button)

        layout4.addWidget(hobby_box)
        layout4.addLayout(layout5)
        hobby_box2.setLayout(layout4)

        self.controls[biaoqian] = dongdai_chuangjian_lst
        self.controls2[biaoqian] = hobby_box2
        self.zuixin_hobby_box2 = hobby_box2
        self.count += 1

    def add_clicked(self):
        self.add_kongjianzu()
        self.scroll_layout.addWidget(self.zuixin_hobby_box2)

    def remove_clicked(self):
        self.queren_msg.setText("你确定要【删除最后一个控件组】吗？")
        # 显示对话框并获取用户的选择
        result = self.queren_msg.exec_()
        if result == QMessageBox.Yes:
            # 从控件列表中移除最后一个控件
            if self.controls2:
                zuihou_k = ''
                for x in self.controls2.keys():
                    zuihou_k = x
                    break
                qg_zuihou_v = self.controls2[zuihou_k]
                qg_zuihou_v.setParent(None)

                del self.controls[zuihou_k]
                del self.controls2[zuihou_k]

    def print_clicked(self):
        try:
            if re.findall(r'\'(.+?)_基础数据_', str(self.controls)):
                jiaoben_lst = natsort.natsorted(os.listdir(r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\shishicesi\spiders'))
                zuixin_bianhao = str(int(re.findall(r'\d+', jiaoben_lst[-3])[0]) + 1)
                jiaoben_lst_str = str(jiaoben_lst)
                for k, v in self.controls.items():
                    if '_基础数据_' in k:
                        if v[1].text() in jiaoben_lst_str:
                            yicunzai_bianhao_jiaoben_name = re.findall("'(\d+){}".format(v[1].text()), jiaoben_lst_str)[0] + v[1].text()
                            self.queren_msg.setText("发现已有脚本：{}\n是否还要创建：{}{}".format(yicunzai_bianhao_jiaoben_name, zuixin_bianhao, v[1].text()))
                            # 显示对话框并获取用户的选择
                            result = self.queren_msg.exec_()
                            if result == QMessageBox.Yes:
                                chuangjian_luoji.chuangjian(self.controls, zuixin_bianhao)
                        else:
                            self.queren_msg.setText("你确定要【创建：{}{}】吗？".format(zuixin_bianhao, v[1].text()))
                            # 显示对话框并获取用户的选择
                            result = self.queren_msg.exec_()
                            if result == QMessageBox.Yes:
                                chuangjian_luoji.chuangjian(self.controls, zuixin_bianhao)
        except:
            QMessageBox.warning(self, "错误", f"发生了一个错误：{traceback.format_exc()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
