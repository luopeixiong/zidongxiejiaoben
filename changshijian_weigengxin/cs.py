import random
import math

lst = ((1, 'a'), (2, 'b'), (3, 'c'))
zuiji_sige_xuanxiang_lst = random.sample(lst, 4)
print(zuiji_sige_xuanxiang_lst)




class cs:
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost", user="root", passwd="123456", database="shen_hui_fu",
            charset="utf8"
            )
        self.cursor = self.conn.cursor()

    def xieru_ci(self, danci_yisi_dic):
        sql = "select id, danci from yicun_danci where danci = '%s';" % self.word
        self.cursor.execute(sql)
        shuju = self.cursor.fetchone()
        self.conn.commit()  # 刷新数据，用来写入的
        if not shuju:
            sql = "INSERT INTO yicun_danci(danci, zhengque_num, yisi) VALUES ('%s', 0, '%s');" % (self.word, json.dumps(danci_yisi_dic).encode('utf-8').decode('unicode_escape'))
            self.cursor.execute(sql)
            self.conn.commit()  # 刷新数据，用来写入的

    def get_sige_xuanxiang(self):
        pingjunzhi = 0
        xiaoyudengyu_pingjunzhi_sql = "select * from yicun_danci where zhengque_num <= %s;" % math.ceil(pingjunzhi)
        self.cursor.execute(xiaoyudengyu_pingjunzhi_sql)
        xiaoyudengyu_pingjunzhi_shuju = self.cursor.fetchone()
        self.conn.commit()  # 刷新数据，用来写入的
        zuiji_sige_xuanxiang_lst = random.sample(xiaoyudengyu_pingjunzhi_shuju, 1)
        dayu_pingjunzhi_sql = "select * from yicun_danci where zhengque_num <= %s;" % math.ceil(pingjunzhi)
        self.cursor.execute(dayu_pingjunzhi_sql)
        dayu_pingjunzhi_shuju = self.cursor.fetchone()
        self.conn.commit()  # 刷新数据，用来写入的
        if len(dayu_pingjunzhi_shuju) <= 3:
        zuiji_sige_xuanxiang_lst = random.sample(dayu_pingjunzhi_shuju, 3)

    def xieru_ju(self):
        juzi = ''
        sql = "select id, danci from yicun_juzi where juzi = '%s';" % juzi
        self.cursor.execute(sql)
        shuju = self.cursor.fetchone()
        self.conn.commit()  # 刷新数据，用来写入的
        if not shuju:
            sql = "INSERT INTO yicun_juzi(danci, zhengque_num, yisi) VALUES ('%s', 0, '%s');" % (self.word, json.dumps(danci_yisi_dic).encode('utf-8').decode('unicode_escape'))
            self.cursor.execute(sql)
            self.conn.commit()  # 刷新数据，用来写入的

