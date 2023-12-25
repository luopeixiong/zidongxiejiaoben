import math
from funboost import boost, BrokerEnum
import requests
import json
import threading
import re
import pymysql

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用InsecureRequestWarning警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

lock = threading.Lock()


# # 连接到数据库（如果文件不存在，它将创建一个新的数据库文件）
# conn = pymysql.connect(
#     host='localhost',  # 主机名
#     user='root',  # 用户名
#     password='123456',  # 密码
#     database='weipa_funt'  # 数据库名
# )
#
# # 创建一个游标对象
# cursor = conn.cursor()
#
#
# guanjianzi_lst = ['采购', '招标', '中选', '成交', '废标', '流标', '询价', '代理', '磋商', '结果']
# a = ''
# b = '%s, %s, '
# for index, z in enumerate(guanjianzi_lst):
#     if (index + 1) != len(guanjianzi_lst):
#         a += '{}, '.format(z)
#         b += '%s, '
#     else:
#         a += '{}'.format(z)
#         b += '%s'
#
# insert_sql = "INSERT INTO users (title, url, %s) VALUES (%s)" % (a, b)
#
#
# # 检查表A是否存在
# table_name = 'users'
# cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
#
# # 如果表A存在，则删除它
# if cursor.fetchone():
#     cursor.execute(f"DROP TABLE {table_name}")
#     print(f"表{table_name}已删除。")
# else:
#     print(f"表{table_name}不存在。")
#
#
# create_sql = 'CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), url VARCHAR(255), '
# for index, y in enumerate(guanjianzi_lst):
#     if (index+1) != len(guanjianzi_lst):
#         create_sql += '{} INT, '.format(y)
#     else:
#         create_sql += '{} INT)'.format(y)
# cursor.execute(create_sql)
# # 提交更改
# conn.commit()


class Lei:
    def __init__(self):
        self.gov_url_list = []

@boost('req_name', broker_kind=BrokerEnum.REDIS, max_retry_times=1)
def req():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    response = requests.post('https://www.gxdx.gov.cn/', headers=headers, timeout=5, verify=False).content.decode('utf-8')
    url_lst = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", response)
    for url in url_lst:
        quanduan_url = '/'.join(url.split('/')[:3])
        if 'gov.cn' in quanduan_url:
            with lock:
                if quanduan_url not in lei.gov_url_list:
                    print(quanduan_url)
                    lei.gov_url_list.append(quanduan_url)
                    with open(r'D:\pycharm_xiangmu\zidongxiejiaoben\funt_jiaoben_cs\党校url.json', 'w', encoding='utf-8') as f:
                        json.dump(lei.gov_url_list, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    lei = Lei()
    req.clear()  # 清空列表页
    req.push()  # 启动列表页生产
    req.consume()  # 启动列表页消费
