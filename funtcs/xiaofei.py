import requests
from funboost import boost, BrokerEnum
from datetime import datetime
import time


@boost('liebiao_name', broker_kind=BrokerEnum.REDIS_ACK_ABLE)
def liebiao(news_type, page):
    start_time = datetime.now()
    print('第 {} 页启动 {}'.format(page, start_time))
    headers = {
        'authority': 'api.bilibili.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'cookie': "_uuid=387210A87-8ED2-A10F9-38F8-98D721452107488957infoc; buvid3=04F31225-AB31-A274-755E-D634844C725C91665infoc; b_nut=1672643990; buvid4=ACFA68BE-8329-25DB-0064-A34226CCD16291665-023010215-6Xjdpy7h1VS0yCHtPI5qkg%3D%3D; i-wanna-go-back=-1; buvid_fp_plain=undefined; b_ut=5; rpdid=|(J|km|Y||u|0J'uY~JRlkumk; nostalgia_conf=-1; hit-dyn-v2=1; LIVE_BUVID=AUTO6916763727148592; header_theme_version=CLOSE; CURRENT_PID=2d7c0490-cd55-11ed-9c9b-0f2aeefd6050; hit-new-style-dyn=1; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; FEED_LIVE_VERSION=V8; bp_video_offset_1317489508=822479880644984835; bp_video_offset_172835037=827137059727605815; dy_spec_agreed=1; bp_video_offset_508977422=829344445264560144; DedeUserID=3537117921676014; DedeUserID__ckMd5=b9db6882a6780827; CURRENT_QUALITY=80; fingerprint=facbbbe31c1e2a2b74de482a1d12d324; buvid_fp=facbbbe31c1e2a2b74de482a1d12d324; SESSDATA=62a953bf%2C1708619029%2Cf8112%2A81-WldB595WLIucKH8fXnZXp4fPy9aDN1XzFPRBnVxyF0wAdJKx3W96nyn1IHQzy1Mag2Q9QAADgA; bili_jct=a7f08fc1f8505823e4c62965bfa37c8c; home_feed_column=5; bp_video_offset_3537117921676014=834526607035072535; share_source_origin=COPY; bsource=share_source_copy_link; b_lsid=10104A7424_18A37706E6E; browser_resolution=1707-840; sid=4ogkwncl; bili_ticket=eyJhbGciOiJFUzM4NCIsImtpZCI6ImVjMDIiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2OTM0MDg4MDQsImlhdCI6MTY5MzE0OTYwNCwicGx0IjotMX0.9zvNntee1-ObgZs9YFqPEs_sBaWOKaxdzWQDbik83Hexcl3aBdR95006CvcNwuVO6-h8n2YwaPbD353z3svocBSZS-CMYaHpvwIQeFW8gL2siMURvDvBc77AKJSfdwGQ; bili_ticket_expires=1693408804; PVID=3",
        'origin': 'https://space.bilibili.com',
        'pragma': 'no-cache',
        'referer': 'https://space.bilibili.com/486906719/video',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    params = {
        'mid': '486906719',
        'ps': '30',
        'tid': '0',
        'pn': str(page),
        'keyword': '',
        'order': 'pubdate',
        'platform': 'web',
        'web_location': '1550101',
        'order_avoided': 'true',
        'w_rid': 'fa38881a4c9a8589e062dded77758535',
        'wts': str(time.time()),
    }
    response = requests.get('https://api.bilibili.com/x/space/wbi/arc/search', params=params, headers=headers).json()  # video_list
    Count = response["data"]["page"]
    print('第 {} 页爬取完毕： {} '.format(page, Count))
    end_time = datetime.now()
    # 计算时间差值
    elapsed_time = end_time - start_time

    # 获取时间差值中的秒数和微秒数
    seconds = elapsed_time.seconds
    microseconds = elapsed_time.microseconds
    print('第 {} 页结束 {}，花费 {} 秒, {} 微秒'.format(page, end_time, seconds, microseconds))
    return Count


if __name__ == '__main__':
    liebiao.consume()  # 启动列表页消费
