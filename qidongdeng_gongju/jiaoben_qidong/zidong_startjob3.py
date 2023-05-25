import sys
import time
import traceback
from datetime import datetime
import natsort
import requests
from random import shuffle
import platform


class Scrapyd:
    def __init__(self):
        self.gongju_lst = None
        if platform.system() == "Windows":
            self.urls = 'http://192.168.0.233:6800'
        elif platform.system() == "Linux":
            self.urls = 'http://127.0.0.1:6800'
        self.biaoxun_lst = []
        self.zixun_lst = []
        self.url_liebiao_str = ['shishizixun|0url列表查找']
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
                    shuffle(self.zixun_lst)  # 当一直重启程序时不至于老跑前面那几个脚本
                elif 'gongju' in x:
                    self.gongju_lst = natsort.natsorted(['{}|{}'.format(x, i) for i in spiders])
                    shuffle(self.gongju_lst)  # 当一直重启程序时不至于老跑前面那几个脚本
                else:
                    self.biaoxun_lst = natsort.natsorted(['{}|{}'.format(x, i) for i in spiders])
                    shuffle(self.biaoxun_lst)  # 当一直重启程序时不至于老跑前面那几个脚本

    def qidong(self):
        if platform.system() == "Windows":
            with open(r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\jiancha_jiaoben_chaoshi\job3_heimingdan.txt', 'r', encoding='utf-8') as f:
                job_heimingdan_lst = f.read().split('\n')
        elif platform.system() == "Linux":
            with open('/www/wwwroot/bcy/qidongdeng_gongju/jiancha_jiaoben_chaoshi/job3_heimingdan.txt', 'r', encoding='utf-8') as f:
                job_heimingdan_lst = f.read().split('\n')
        for liebiao in [self.biaoxun_lst, self.zixun_lst]:
            for x in liebiao:
                if str(x.split('|')[1]) not in str(job_heimingdan_lst):
                    while True:
                        resp = requests.get(url='{}/listjobs.json'.format(self.urls))
                        if len(resp.json()['running']) < 30:
                            r = requests.post(url=self.urls + '/schedule.json', data=('project=' + str(x.split('|')[0]) + '&spider=' + str(x.split('|')[1])).encode('utf-8'), headers=self.headers)
                            html = r.json()
                            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            if html['status'] == 'ok':
                                pass
                            else:
                                print('失败：{}{}{}'.format(x, html['jobid'], ts))
                            break
                        else:
                            time.sleep(2)
                else:
                    print('出现黑名单：{}'.format(x))
                time.sleep(1)


if __name__ == '__main__':
    try:
        scrapyd = Scrapyd()
        while True:
            scrapyd.projects()
            scrapyd.qidong()
            sys.stdout.flush()
            time.sleep(60 * 30)
    except:
        print(traceback.print_exc())
