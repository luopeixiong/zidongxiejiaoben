import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QPushButton, \
    QLineEdit, QComboBox, QLabel, QTextEdit

import chuangjian_get_gui
import json


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        with open('gui_data.json', 'r', encoding='utf8') as f:
            self.kongjian_text_data = json.load(f)
        self.setWindowTitle('get一般模板')
        self.resize(500, 500)
        self.kongjian_dict = {}

        self.container = QVBoxLayout()

        self.box_0 = QGroupBox()
        self.box_1 = QGroupBox()
        self.box_2 = QGroupBox()
        self.box_3 = QGroupBox()
        self.box_4 = QGroupBox()
        self.box_5 = QGroupBox()
        self.box_10 = QGroupBox()

        self.layout = QVBoxLayout()
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QVBoxLayout()
        self.layout4 = QVBoxLayout()
        self.layout5 = QVBoxLayout()
        self.layout10 = QHBoxLayout()

        self.def0()

        self.def1()

        self.def2()

        self.def3()

        self.def4()

        self.def5()

        self.def10()

        self.box_0.setLayout(self.layout)
        self.box_1.setLayout(self.layout1)
        self.box_2.setLayout(self.layout2)
        self.box_3.setLayout(self.layout3)
        self.box_4.setLayout(self.layout4)
        self.box_5.setLayout(self.layout5)
        self.box_10.setLayout(self.layout10)

        self.container.addWidget(self.box_0)
        self.container.addWidget(self.box_1)
        self.container.addWidget(self.box_2)
        self.container.addWidget(self.box_3)
        self.container.addWidget(self.box_4)
        self.container.addWidget(self.box_5)
        self.container.addWidget(self.box_10)

        self.setLayout(self.container)

    def def0(self):
        label_lst = ['脚本编号：', '脚本中文名：', '脚本类名：', '脚本域名：']
        shurukuang_lst = []

        bianhao_LineEdit = QLineEdit()
        bianhao_LineEdit.setText(self.kongjian_text_data['脚本编号'])
        bianhao_LineEdit.setGeometry(55, 20, 200, 20)
        shurukuang_lst.append(bianhao_LineEdit)
        self.kongjian_dict['编号'] = bianhao_LineEdit

        zhongwen_ming_LineEdit = QLineEdit()
        zhongwen_ming_LineEdit.setText(self.kongjian_text_data['脚本中文名'])
        zhongwen_ming_LineEdit.setGeometry(55, 20, 200, 20)
        shurukuang_lst.append(zhongwen_ming_LineEdit)
        self.kongjian_dict['中文名'] = zhongwen_ming_LineEdit

        class_name_LineEdit = QLineEdit()
        class_name_LineEdit.setText(self.kongjian_text_data['脚本类名'])
        class_name_LineEdit.setGeometry(55, 20, 200, 20)
        shurukuang_lst.append(class_name_LineEdit)
        self.kongjian_dict['类名'] = class_name_LineEdit

        for x in range(len(shurukuang_lst)):
            label = QLabel(label_lst[x])
            self.layout.addWidget(label)
            self.layout.addWidget(shurukuang_lst[x])

    def def1(self):
        qishi_url_TextEdit = QTextEdit()
        qishi_url_TextEdit.setGeometry(55, 20, 200, 20)
        qishi_url_TextEdit.setAcceptRichText(False)
        qishi_url_TextEdit.setFontFamily("黑体")  # 字体设置为黑体
        qishi_url_TextEdit.setText(self.kongjian_text_data['起始url_lst'])
        self.kongjian_dict['起始url_lst'] = qishi_url_TextEdit
        label = QLabel('脚本起始url')
        self.layout1.addWidget(label)
        self.layout1.addWidget(qishi_url_TextEdit)

    def def2(self):
        label_lst = ['列表title-xpath：', '列表url-xpath：', '列表时间-xpath：', '列表时间-re：']
        shurukuang_lst = []

        liebiao_biaoti_xpath_LineEdit = QLineEdit()
        liebiao_biaoti_xpath_LineEdit.setText(self.kongjian_text_data['列表title-xpath'])
        liebiao_biaoti_xpath_LineEdit.setGeometry(55, 20, 200, 20)
        shurukuang_lst.append(liebiao_biaoti_xpath_LineEdit)
        self.kongjian_dict['列表标题-xpath'] = liebiao_biaoti_xpath_LineEdit

        liebiao_url_xpath_LineEdit = QLineEdit()
        liebiao_url_xpath_LineEdit.setText(self.kongjian_text_data['列表url-xpath'])
        liebiao_url_xpath_LineEdit.setGeometry(55, 20, 200, 20)
        shurukuang_lst.append(liebiao_url_xpath_LineEdit)
        self.kongjian_dict['列表url-xpath'] = liebiao_url_xpath_LineEdit

        liebiao_publishtime_xpath_LineEdit = QLineEdit()
        liebiao_publishtime_xpath_LineEdit.setText(self.kongjian_text_data['列表时间-xpath'])
        liebiao_publishtime_xpath_LineEdit.setGeometry(55, 20, 200, 20)
        shurukuang_lst.append(liebiao_publishtime_xpath_LineEdit)
        self.kongjian_dict['列表时间-xpath'] = liebiao_publishtime_xpath_LineEdit

        liebiao_publishtime_re_LineEdit = QLineEdit()
        liebiao_publishtime_re_LineEdit.setText(self.kongjian_text_data['列表时间-re'])
        liebiao_publishtime_re_LineEdit.setGeometry(55, 20, 200, 20)
        shurukuang_lst.append(liebiao_publishtime_re_LineEdit)
        self.kongjian_dict['列表时间-re'] = liebiao_publishtime_re_LineEdit

        for x in range(len(shurukuang_lst)):
            label = QLabel(label_lst[x])
            self.layout2.addWidget(label)
            self.layout2.addWidget(shurukuang_lst[x])

    def def3(self):
        # 下拉列表
        self.zhaobiao_wenjian_name_ComboBox = QComboBox()
        self.zhaobiao_wenjian_name_ComboBox.addItems(['zhaobiao2', 'zhaobiao3'])
        # 信号
        # self.cb.currentIndexChanged[str].connect(self.click_my_btn)  # 条目发生改变，发射信号，传递条目内容
        # self.zhaobiao_wenjian_name_ComboBox.currentIndexChanged[int].connect(self.click_my_btn)  # 条目发生改变，发射信号，传递条目内容
        self.layout3.addWidget(self.zhaobiao_wenjian_name_ComboBox)
        self.kongjian_dict['招标方案-文件名'] = self.zhaobiao_wenjian_name_ComboBox

        self.def3_zhaobiao_urlpanduan_biaotipanduan_LineEdit = QLineEdit()
        self.def3_zhaobiao_urlpanduan_biaotipanduan_LineEdit.setGeometry(55, 20, 200, 20)
        self.layout3.addWidget(self.def3_zhaobiao_urlpanduan_biaotipanduan_LineEdit)
        self.kongjian_dict['招标url-标题判断'] = self.def3_zhaobiao_urlpanduan_biaotipanduan_LineEdit

    def def4(self):
        # 下拉列表
        self.fanye_fangan_wenjianjia_name_ComboBox = QComboBox()
        self.fanye_fangan_wenjianjia_name_ComboBox.addItems(['fanye1', 'fanye2'])
        # 信号
        self.fanye_fangan_wenjianjia_name_ComboBox.currentIndexChanged[str].connect(self.click_my_btn)  # 条目发生改变，发射信号，传递条目内容
        # self.fanye_fangan_wenjianjia_name_ComboBox.currentIndexChanged[int].connect(self.click_my_btn)  # 条目发生改变，发射信号，传递条目内容
        self.layout4.addWidget(self.fanye_fangan_wenjianjia_name_ComboBox)
        self.kongjian_dict['翻页方案-文件名'] = self.fanye_fangan_wenjianjia_name_ComboBox

        self.fanan_xpath_LineEdit = QLineEdit()
        self.fanan_xpath_LineEdit.setText(self.kongjian_text_data['翻页-xpath'])
        self.fanan_xpath_LineEdit.setGeometry(55, 20, 200, 20)
        self.layout4.addWidget(self.fanan_xpath_LineEdit)
        self.kongjian_dict['翻页-xpath'] = self.fanan_xpath_LineEdit

        self.fanan2_LineEdit = QLineEdit()
        self.fanan_xpath_LineEdit.setGeometry(55, 20, 200, 20)
        self.layout4.addWidget(self.fanan2_LineEdit)
        self.kongjian_dict['翻页2'] = self.fanan2_LineEdit

    def def5(self):
        zhengwen_title_xpath_LineEdit = QLineEdit()
        zhengwen_title_xpath_LineEdit.setGeometry(55, 20, 200, 20)
        zhengwen_title_xpath_LineEdit.setText(self.kongjian_text_data['正文title-xpath'])
        self.kongjian_dict['正文title-xpath'] = zhengwen_title_xpath_LineEdit
        label = QLabel('正文title-xpath')
        self.layout5.addWidget(label)
        self.layout5.addWidget(zhengwen_title_xpath_LineEdit)

        zhengwen_publishtime_xpath_LineEdit = QLineEdit()
        zhengwen_publishtime_xpath_LineEdit.setGeometry(55, 20, 200, 20)
        zhengwen_publishtime_xpath_LineEdit.setText(self.kongjian_text_data['正文时间-xpath'])
        self.kongjian_dict['正文时间-xpath'] = zhengwen_publishtime_xpath_LineEdit
        label = QLabel('正文时间-xpath')
        self.layout5.addWidget(label)
        self.layout5.addWidget(zhengwen_publishtime_xpath_LineEdit)

        zhengwen_publishtime_re_LineEdit = QLineEdit()
        zhengwen_publishtime_re_LineEdit.setGeometry(55, 20, 200, 20)
        zhengwen_publishtime_re_LineEdit.setText(self.kongjian_text_data['正文时间-re'])
        self.kongjian_dict['正文时间-re'] = zhengwen_publishtime_re_LineEdit
        label = QLabel('正文时间-re')
        self.layout5.addWidget(label)
        self.layout5.addWidget(zhengwen_publishtime_re_LineEdit)

        zhengwen_content_xpath_LineEdit = QLineEdit()
        zhengwen_content_xpath_LineEdit.setGeometry(55, 20, 200, 20)
        zhengwen_content_xpath_LineEdit.setText(self.kongjian_text_data['正文内容-xpath'])
        self.kongjian_dict['正文内容-xpath'] = zhengwen_content_xpath_LineEdit
        label = QLabel('正文内容-xpath')
        self.layout5.addWidget(label)
        self.layout5.addWidget(zhengwen_content_xpath_LineEdit)

    def def10(self):
        btn1 = QPushButton('创建')
        btn1.clicked.connect(self.get_Data)
        self.layout10.addWidget(btn1)
        btn2 = QPushButton('保存')
        btn2.clicked.connect(self.baocun_Data)
        self.layout10.addWidget(btn2)

    def click_my_btn(self, i):
        print(i)
        print(self.zhaobiao_wenjian_name_ComboBox.currentText())
        if i == 'fanye1':
            self.fanan_xpath_LineEdit.setEnabled(True)
            self.fanan2_LineEdit.setEnabled(False)
        elif i == 'fanye2':
            self.fanan_xpath_LineEdit.setEnabled(False)
            self.fanan2_LineEdit.setEnabled(True)
        print('---------------')

    def get_Data(self):
        self.baocun_Data()
        chuangjian_get_gui.chuangjian_get(self.kongjian_dict)

    def baocun_Data(self):
        with open("gui_data.json", "r", encoding="utf-8") as f:
            old_data = json.load(f)
            old_data["脚本编号"] = self.kongjian_dict['编号'].text()
            old_data["脚本中文名"] = self.kongjian_dict['中文名'].text()
            old_data["脚本类名"] = self.kongjian_dict['类名'].text()
            old_data["起始url_lst"] = self.kongjian_dict['起始url_lst'].toPlainText()
            old_data["列表title-xpath"] = self.kongjian_dict['列表标题-xpath'].text()
            old_data["列表url-xpath"] = self.kongjian_dict['列表url-xpath'].text()
            old_data["列表时间-xpath"] = self.kongjian_dict['列表时间-xpath'].text()
            old_data["列表时间-re"] = self.kongjian_dict['列表时间-re'].text()
            old_data["翻页-xpath"] = self.kongjian_dict['翻页-xpath'].text()
            old_data["正文title-xpath"] = self.kongjian_dict['正文title-xpath'].text()
            old_data["正文时间-xpath"] = self.kongjian_dict['正文时间-xpath'].text()
            old_data["正文时间-re"] = self.kongjian_dict['正文时间-re'].text()
            old_data["正文内容-xpath"] = self.kongjian_dict['正文内容-xpath'].text()
        with open("gui_data.json", "w", encoding="utf-8") as f:
            json.dump(old_data, f, ensure_ascii=False, indent=4)
        print('保存完毕')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()

    w.show()
    app.exec()
