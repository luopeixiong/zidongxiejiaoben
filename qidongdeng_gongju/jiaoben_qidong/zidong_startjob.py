from datetime import datetime
import requests
import time
import natsort


class Scrapyd:
    def __init__(self):
        self.urls = 'http://192.168.0.233:6800'
        self.biaoxun_lst = []
        self.zixun_lst = []
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    def projects(self):  # 获取项目
        r = requests.get(url=self.urls + '/listprojects.json')
        if 'projects' in r.json():
            projects = r.json()['projects']  # ['shishicesi', 'shishizixun']
            for x in projects:
                r1 = requests.get(url=self.urls + '/listspiders.json?project=' + str(x))
                spiders = r1.json()['spiders']
                if 'zixun' in x:
                    self.zixun_lst = natsort.natsorted(['{}|{}'.format(x, i) for i in spiders])
                else:
                    self.biaoxun_lst = natsort.natsorted(['{}|{}'.format(x, i) for i in spiders])

    def qidong(self):
        with open('job3_heimingdan.txt', 'r', encoding='utf-8') as f:
            job_heimingdan_lst = f.read().split('\n')
        for liebiao in [self.zixun_lst, self.biaoxun_lst]:
            for x in liebiao:
                if str(x.split('|')[1]) not in str(job_heimingdan_lst):
                    r = requests.post(url=self.urls + '/schedule.json', data=('project=' + str(x.split('|')[0]) + '&spider=' + str(x.split('|')[1])).encode('utf-8'), headers=self.headers)
                    html = r.json()
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if html['status'] == 'ok':
                        print('成功：{}{}{}'.format(x, html['jobid'], ts))
                    else:
                        print('失败：{}{}{}'.format(x, html['jobid'], ts))
                else:
                    print('出现黑名单：{}'.format(x))
                time.sleep(0.5)


if __name__ == '__main__':
    scrapyd = Scrapyd()
    scrapyd.projects()
    while True:
        scrapyd.qidong()
