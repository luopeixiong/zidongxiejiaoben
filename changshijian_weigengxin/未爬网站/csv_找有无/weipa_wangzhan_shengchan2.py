import math
from funboost import boost, BrokerEnum
import requests
import json
import threading
import re
from bs4 import BeautifulSoup
import pymysql
import pandas as pd
import csv

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用InsecureRequestWarning警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

lock = threading.Lock()
# 连接到数据库（如果文件不存在，它将创建一个新的数据库文件）
conn = pymysql.connect(
    host='localhost',  # 主机名
    user='root',  # 用户名
    password='123456',  # 密码
    database='weipa_funt'  # 数据库名
)

# 创建一个游标对象
cursor = conn.cursor()


guanjianzi_lst = ['采购', '招标', '中选', '成交', '废标', '流标', '询价', '代理', '磋商', '结果']
a = ''
b = '%s, %s, '
for index, z in enumerate(guanjianzi_lst):
    if (index + 1) != len(guanjianzi_lst):
        a += '{}, '.format(z)
        b += '%s, '
    else:
        a += '{}'.format(z)
        b += '%s'

insert_sql = "INSERT INTO users (title, url, %s) VALUES (%s)" % (a, b)


# 检查表A是否存在
table_name = 'users'
cursor.execute(f"SHOW TABLES LIKE '{table_name}'")

# 如果表A存在，则删除它
if cursor.fetchone():
    cursor.execute(f"DROP TABLE {table_name}")
    print(f"表{table_name}已删除。")
else:
    print(f"表{table_name}不存在。")


create_sql = 'CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), url VARCHAR(255), '
for index, y in enumerate(guanjianzi_lst):
    if (index+1) != len(guanjianzi_lst):
        create_sql += '{} INT, '.format(y)
    else:
        create_sql += '{} INT)'.format(y)
cursor.execute(create_sql)
# 提交更改
conn.commit()


def xieru_sqlite(k, dic):
    yuanzu = [dic['title'], dic['url']]
    for x in guanjianzi_lst:
        yuanzu.append(dic[x])
    cursor.execute(insert_sql, yuanzu)
    # 提交更改
    conn.commit()


@boost('guanjianci_guolu_name', broker_kind=BrokerEnum.REDIS, max_retry_times=1)
def guanjianci_guolu(dic):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    try:
        html_text = requests.get(dic['url'], headers=headers, timeout=10, verify=False).content.decode('utf-8')
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(html_text, 'html.parser')
        # 使用find_all方法找到所有的a标签
        a_tags = soup.find_all('a')
        meiyou_guanjianzi = True
        for x in guanjianzi_lst:
            num = str(a_tags).count(x)
            dic[x] = num
            if num:
                meiyou_guanjianzi = False

        if meiyou_guanjianzi:
            print('NO：{}'.format(dic['title']))
            with lock:
                # xieru('未找到', dic)
                xieru_sqlite('未找到', dic)
        else:
            print('YES：{}'.format(dic['title']))
            with lock:
                # xieru('找到', dic)
                xieru_sqlite('找到', dic)
    except:
        print('ERR：{}'.format(dic['title']))
        for x in guanjianzi_lst:
            num = str('').count(x)
            dic[x] = num
        with lock:
            # xieru('报错', dic)
            xieru_sqlite('报错', dic)


def main():
    # 打开CSV文件
    with open('uncrawledsource.csv', 'r', encoding='utf-8') as file:
        # 创建CSV读取器
        csv_reader = csv.reader(file)
        # 遍历每一行
        for row in csv_reader:
            if str(row[0]) != '':
                dic = {'url': row[0], 'title': row[3]}
                # 在这里使用你获取到的数据进行处理
                # print(dic)
            guanjianci_guolu.push(dic)
    guanjianci_guolu.consume()


if __name__ == '__main__':
    main()
