# -*- coding:utf-8 -*-
import time

import binjie
import wwccoo
import xiaofuge
import pymysql
import json
import logging
import traceback
import sys
import os
import platform


# 协程不懂怎么用自写的print_log来记日志，只能单这样写
# 定义一个 StreamToLogger 类
class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


class BieRenGpt:
    def __init__(self):
        self.zaoju_num = None
        self.yuan_danci_lst = None
        self.wanzheng_dic_lst = []
        self.baocuo = False
        self.msg = ''
        self.linshi_baocun = ''
        system = platform.system()
        if system == 'Windows':
            self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="123456", database="yingyu", charset="utf8")
        elif system == 'Linux':
            self.conn = pymysql.connect(host="127.0.0.1", user="yingyu", passwd="caonima123123", database="yingyu", charset="utf8")
        else:
            self.conn = pymysql.connect(host="127.0.0.1", user="yingyu", passwd="caonima123123", database="yingyu", charset="utf8")
        # (3)创建游标(新建查询会话)，通过游标执行SQL语句
        self.cursor = self.conn.cursor()
        self.shuju = []

    def get_data(self):
        sql = "select * from app01_gpt_duilie;"
        self.cursor.execute(sql)
        self.shuju = self.cursor.fetchall()
        self.conn.commit()

    def get_juzi(self, yuan_danci_lst):
        self.yuan_danci_lst = eval(yuan_danci_lst[3])
        self.zaoju_num = 1
        self.msg = '现在我告诉你一会你要发送给我消息的规则：1.首先我会告诉你要造句的单词有哪些，并且造出的句子的规则有哪些，然后你返回给我你造出的句子的方式。以下是例子，我：请用这三个单词 how，finish，my，造出三个句子，并且造出的句子尽量有这三个单词。你：以下是我造出的三个句子以及对应数据的整理：《{"造出的句子":"how can I finish work?","造出句子的中文意思":"我怎样才能完成工作？","造出此句的源单词和其中文意思":{"how":{"中文意思":"怎样","正确数":0},"finish":{"中文意思":"完成","正确数":0}},"这个句子的介词短语和其中文意思":{},"除了造出此句的源单词以外的其他单词的意思":{"can":{"中文意思":"能够","正确数":0},"I":{"中文意思":"我","正确数":0},"work":{"中文意思":"工作","正确数":0}}},{"造出的句子":"how can I finish my homework before dinner?","造出句子的中文意思":"我怎样才能在晚餐前完成我的家庭作业？","造出此句的源单词和其中文意思":{"how":{"中文意思":"怎样","正确数":0},"finish":{"中文意思":"完成","正确数":0},"my":{"中文意思":"我的","正确数":0}},"这个句子的介词短语和其中文意思":{"before dinner":{"中文意思":"晚餐前","正确数":0}},"除了造出此句的源单词以外的其他单词的意思":{"can":{"中文意思":"能够","正确数":0},"I":{"中文意思":"我","正确数":0},"homework":{"中文意思":"家庭作业","正确数":0}}},{"造出的句子":"how can finish work before the deadline?","造出句子的中文意思":"我怎样才能在截止日期之前完成工作？","造出此句的源单词和其中文意思":{"how":{"中文意思":"怎样","正确数":0},"finish":{"中文意思":"完成","正确数":0}},"这个句子的介词短语和其中文意思":{"before the deadline":{"中文意思":"在截止日期之前","正确数":0}},"除了造出此句的源单词以外的其他单词的意思":{"can":{"中文意思":"能够","正确数":0},"work":{"中文意思":"工作","正确数":0}}}》。请以以上的规则来回复我的造句要求，'
        self.msg += '请用这{}个单词 {}，造出{}个句子，并且造出的句子必须有这{}个单词'.format(len(self.yuan_danci_lst), '，'.join(self.yuan_danci_lst), self.zaoju_num, len(self.yuan_danci_lst))
        binjie.main(self)
        return self.wanzheng_dic_lst

    def xieru_juzi(self, sql_lst, juzi_dic):
        danci_dic = {}
        danci_dic.update(juzi_dic['这个句子的介词短语和其中文意思'])
        danci_dic.update(juzi_dic['造出此句的源单词和其中文意思'])
        danci_dic.update(juzi_dic['除了造出此句的源单词以外的其他单词的意思'])
        danci_dic = json.dumps(danci_dic, ensure_ascii=False)
        sql = f"INSERT INTO app01_yicun_juzi (yinyu_juzi, zhongwen_yisi, meige_danci_yisi, yonghu_id) VALUES ('%s','%s','%s',%s);" % (juzi_dic['造出的句子'].replace("'", "’"), juzi_dic['造出句子的中文意思'], danci_dic.replace("'", "’"), sql_lst[1])
        self.cursor.execute(sql)
        self.conn.commit()  # 刷新数据，用来写入的

    def shanchu_gpt_biao_data(self, sql_lst):
        # 执行删除操作
        sql = "DELETE FROM app01_gpt_duilie WHERE id = %s and yonghu_id = %s" % (sql_lst[0], sql_lst[1])
        self.cursor.execute(sql)
        self.conn.commit()

    def panduan_xinchuang_youwu_yuandanci(self, juzi_dic, sql_lst, zhongzhi):
        for yuan_danci in sql_lst:
            if ''.format(yuan_danci) not in str(juzi_dic):
                print('这个新造的字典没有源单词，禁止写入，并且丢入')
                zhongzhi = True
                break
        return zhongzhi

    def panduan_shifouzai_wufanbiaonei(self, sql_lst):
        where_sql = ''
        for index, y in enumerate(sql_lst):
            if index == 0:
                where_sql = " where wufa_paqu_data LIKE '%{}%'".format(y.replace("'", "’"))
            else:
                where_sql += " and wufa_paqu_data LIKE '%{}%'".format(y.replace("'", "’"))
        sql = "select id, wufa_paqu_data from wufa_paqu {};".format(where_sql)
        self.cursor.execute(sql)
        data_lst = self.cursor.fetchall()
        self.conn.commit()
        if data_lst:
            return 1  # 无法爬取有数据，终止
        else:
            return 0

    def xieru_wufa_paqu(self, sql_lst):
        sql = f"INSERT INTO app01_wufa_paqu (wufa_paqu) VALUES ('%s');" % (str(sql_lst).replace("'", "’"))
        self.cursor.execute(sql)
        self.conn.commit()  # 刷新数据，用来写入的

    def start(self):
        while True:
            self.get_data()
            for sql_lst in self.shuju:
                if self.panduan_shifouzai_wufanbiaonei(sql_lst):
                    print('此组合已在无法爬取写入，终止此组合')
                    self.shanchu_gpt_biao_data(sql_lst)
                    continue
                try:
                    self.get_juzi(sql_lst)
                    for juzi_dic in self.wanzheng_dic_lst:
                        zhongzhi = False
                        zhongzhi = self.panduan_xinchuang_youwu_yuandanci(juzi_dic, sql_lst, zhongzhi)
                        if zhongzhi:
                            self.xieru_wufa_paqu(sql_lst)
                        else:
                            self.xieru_juzi(sql_lst, juzi_dic)
                        self.shanchu_gpt_biao_data(sql_lst)
                except Exception as e:
                    logging.error("主程序抛错：")
                    logging.error(e)
                    logging.error("\n" + traceback.format_exc())
                time.sleep(2)
            time.sleep(10)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    # 设置 log 输出到文件
    logging.basicConfig(
        filename=os.path.join(os.getcwd(), '{}.log'.format(os.path.basename(__file__).split('.')[0])),
        level=logging.DEBUG, filemode='a',
        format='【%(asctime)s】 【%(levelname)s】 >>>  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # 创建 StreamToLogger 实例
    stdout_logger = StreamToLogger(logger, logging.INFO)
    # 将 stdout 重定向到 logger
    sys.stdout = stdout_logger
    print('启动')
    bieren_gpt = BieRenGpt()
    bieren_gpt.start()
