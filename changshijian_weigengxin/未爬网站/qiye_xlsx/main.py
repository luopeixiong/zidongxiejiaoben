from funboost import boost, BrokerEnum
import requests
import threading
import weipa_token2
from bs4 import BeautifulSoup
import pymysql
import pandas as pd

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
b = '%s, %s, %s, '
for index, z in enumerate(guanjianzi_lst):
    if (index + 1) != len(guanjianzi_lst):
        a += '{}, '.format(z)
        b += '%s, '
    else:
        a += '{}'.format(z)
        b += '%s'

insert_sql = "INSERT INTO qiye (title, url, bz, %s) VALUES (%s)" % (a, b)



# 检查表A是否存在
table_name = 'qiye'
cursor.execute(f"SHOW TABLES LIKE '{table_name}'")

# 如果表A存在，则删除它
if cursor.fetchone():
    cursor.execute(f"DROP TABLE {table_name}")
    print(f"表{table_name}已删除。")
else:
    print(f"表{table_name}不存在。")


create_sql = 'CREATE TABLE IF NOT EXISTS qiye (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), url VARCHAR(255), bz VARCHAR(255), '
for index, y in enumerate(guanjianzi_lst):
    if (index + 1) != len(guanjianzi_lst):
        create_sql += '{} INT, '.format(y)
    else:
        create_sql += '{} INT)'.format(y)
cursor.execute(create_sql)
# 提交更改
conn.commit()


def xieru_sqlite(k, dic):
    yuanzu = [dic['title'], dic['url'], dic['bz']]
    for x in guanjianzi_lst:
        yuanzu.append(dic[x])
    cursor.execute(insert_sql, yuanzu)
    # 提交更改
    conn.commit()


@boost('guanjianci_guolu_name', broker_kind=BrokerEnum.REDIS)
def guanjianci_guolu(dic):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    try:
        html_text = requests.get(dic['url'], headers=headers, timeout=10, verify=False).content.decode('utf-8')
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(html_text, 'html.parser')
        # 使用find_all方法找到所有的a标签
        li_tags = soup.find_all('li')
        meiyou_guanjianzi = True
        for x in guanjianzi_lst:
            num = str(li_tags).count(x)
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


@boost('name_guolu_name', broker_kind=BrokerEnum.REDIS)
def name_guolu(dic, cookies):
    json_data = {
        'page': 1,
        'name': '[~]{}'.format(dic['title']),
        'perPage': 20,
        'url': '[~]',
        'create_date': '[-]',
        'update_time': '[-]',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'http://caiji.hangxunbao.com',
        'Pragma': 'no-cache',
        'Referer': 'http://caiji.hangxunbao.com/admin/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }

    params = {
        'page': '1',
        'perPage': '20',
        'orderBy': '',
        'orderDir': '',
    }

    items_name = requests.post(
        'http://caiji.hangxunbao.com/admin/lybiao/list',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    ).json()['data']['items']
    if items_name:  # 如果有此名称，下一步判断url是否有，因为在上面url判断不一定会有
        print('。。。因为其特殊性有名称直接算爬取：' + dic['url'])
        # if dic['url'] in str(items_name):  # 如果url在里面，说明已爬
        #     print('。。。已爬：' + dic['url'])
        # else:  # 如果url不在里面，说明未爬
        #     if dic['bz']:  # 如果此未爬有标签注明标签
        #         print('？？？未爬但标签：' + dic['url'])
        #         guanjianci_guolu.push(dic)
        #     else:
        #         print('！！！未爬：' + dic['url'])
        #         guanjianci_guolu.push(dic)
        #         # guanjianci_guolu(dic)
    else:  # 如果url既没有，也没名称，默认未爬
        if dic['bz']:  # 如果此未爬有标签注明标签
            print('？？？未爬但标签：' + dic['url'])
            guanjianci_guolu.push(dic)
        else:
            print('！！！未爬：' + dic['url'])
            guanjianci_guolu.push(dic)
            # guanjianci_guolu(dic)


@boost('url_guolu_name', broker_kind=BrokerEnum.REDIS)
def url_guolu(dic, cookies):
    json_data = {
        'page': 1,
        'name': '[~]',
        'perPage': 20,
        'url': '[~]{}'.format(dic['yuming']),
        'create_date': '[-]',
        'update_time': '[-]',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'http://caiji.hangxunbao.com',
        'Pragma': 'no-cache',
        'Referer': 'http://caiji.hangxunbao.com/admin/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }

    params = {
        'page': '1',
        'perPage': '20',
        'orderBy': '',
        'orderDir': '',
    }

    items_url = requests.post(
        'http://caiji.hangxunbao.com/admin/lybiao/list',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    ).json()['data']['items']
    if items_url:  # 如果有此url，说明已经被爬
        print('。。。已爬：' + dic['title'])
    else:
        name_guolu.push(dic, cookies)
        # name_guolu(dic, cookies)


def start(cookies):
    # 读取Excel文件
    df = pd.read_excel('qiye.xlsx')
    for index, row in df.iterrows():
        if str(row['网站']) == 'nan':
            title = ''
        else:
            title = row['网站']
        if str(row['bz']) == 'nan':
            bz = ''
        else:
            bz = row['bz']
        if str(row['网址']) != 'nan' or str(row['网址']) != '':
            url = '/'.join(str(row['网址']).split('/')[:3])
            if '//' in str(row['网址']):
                yuming = str(row['网址']).split('/')[2]
            else:
                yuming = str(row['网址'])
            dic = {'title': title, 'bz': bz, 'url': url, 'yuming': yuming}
            # print(dic)
            url_guolu.push(dic, cookies)
        else:
            dic = {'title': title, 'bz': bz, 'url': str(row['网址']), 'yuming': ''}
            with lock:
                xieru_sqlite('报错', dic)


def main():
    url_guolu.clear()
    name_guolu.clear()
    guanjianci_guolu.clear()
    access_token = weipa_token2.main()
    cookies = {
        'Authorization': '"bearer %s"' % access_token,
    }
    start(cookies)
    url_guolu.consume()
    name_guolu.consume()
    guanjianci_guolu.consume()


if __name__ == '__main__':
    main()
