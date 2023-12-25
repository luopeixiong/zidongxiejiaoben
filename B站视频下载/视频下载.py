import os.path
import time
import pymysql
import requests
from fake_useragent import UserAgent


def get_bv(bv, user_agent):

    headers = {
        'authority': 'bili.zhouql.vip',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://zhouql.vip',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
    }

    response = requests.get(f'https://bili.zhouql.vip/meta/{bv}', headers=headers)
    return response


def get_video_url(url, user_agent):
    headers = {
        'authority': 'bili.zhouql.vip',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://zhouql.vip',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
    }

    response = requests.get(url, headers=headers)
    return response


def xiazai_video(video_url, user_agent, bv, title):
    headers = {
        'authority': video_url.split('/')[2],
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://zhouql.vip',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': user_agent,
    }
    response = requests.get(video_url, headers=headers).content
    with open(os.path.join(r'D:\B站下载', f'{title}.mp4'), 'wb') as f:
        f.write(response)


def lianjie_mysql():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="lianxi",  # 引入你想要的在库里创建表
        charset="utf8"
    )
    # (3)创建游标(新建查询会话)，通过游标执行SQL语句
    cursor = conn.cursor()
    return cursor, conn


def main():
    main_path = r"D:\B站下载"
    if not os.path.exists(main_path):
        os.mkdir(main_path)
    cursor, conn = lianjie_mysql()
    sql = "SELECT VIDEO_BVID, VIDEO_TITLE FROM blbl_video_data;"
    cursor.execute(sql)
    with open('断点续传.txt', 'r') as f:
        num = int(f.read())
    # 获取所有结果
    results = cursor.fetchall()

    # 打印结果
    for index, row in enumerate(results):
        if index < num:
            continue
        bv, title = row[0], row[1]
        ua = UserAgent()
        user_agent = ua.Chrome
        response = get_bv(bv, user_agent)
        data_json = response.json()
        url = f'https://bili.zhouql.vip/download/{data_json["data"]["aid"]}/{data_json["data"]["cid"]}'
        response2 = get_video_url(url, user_agent)
        data_json2 = response2.json()
        video_url = data_json2['data']['durl'][0]['url']
        print(video_url)
        xiazai_video(video_url, user_agent, bv, title)
        num += 1
        with open('断点续传.txt', 'w') as f:
            f.write(str(num))
        time.sleep(10)


if __name__ == '__main__':
    main()
