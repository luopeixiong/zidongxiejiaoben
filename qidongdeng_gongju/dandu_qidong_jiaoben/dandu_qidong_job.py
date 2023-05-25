import sys
import traceback
from datetime import datetime
import requests


class Scrapyd:
    def __init__(self):
        self.urls = 'http://127.0.0.1:6800'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    def qidong(self, qidong):
        r = requests.post(url=self.urls + '/schedule.json', data=('project=' + str(qidong.split('|')[0]) + '&spider=' + str(qidong.split('|')[1])).encode('utf-8'), headers=self.headers)
        html = r.json()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if html['status'] == 'ok':
            pass
        else:
            print('失败：{}{}{}'.format(qidong, html['jobid'], ts))


if __name__ == '__main__':
    try:
        qidong = 'gongju|0百度搜索查找'
        scrapyd = Scrapyd()
        scrapyd.qidong(qidong)
        sys.stdout.flush()
    except:
        print(traceback.print_exc())
