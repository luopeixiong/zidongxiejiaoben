import json
import sys
import time
import traceback
from datetime import datetime
import natsort
import requests
from random import shuffle
import platform
import os


class Scrapyd:
    def __init__(self):
        self.gongju_lst = {}
        self.biaoxun_dic = {}
        self.zixun_dic = {}
        self.url_liebiao_str = ['shishizixun|0url列表查找']
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        if platform.system() == "Windows":
            self.urls = 'http://192.168.0.227:6800'

            self.biaoxun_json_path = r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\jiaoben_qidong\判断标讯脚本运行.json'
            self.zixun_json_path = r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\jiaoben_qidong\判断资讯脚本运行.json'
            self.heimingdan_txt_path = r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\jiancha_jiaoben_chaoshi\job3_heimingdan.txt'
        else:
            self.urls = 'http://127.0.0.1:6800'

            self.biaoxun_json_path = '/www/wwwroot/bcy/qidongdeng_gongju/jiaoben_qidong/判断标讯脚本运行.json'
            self.zixun_json_path = '/www/wwwroot/bcy/qidongdeng_gongju/jiaoben_qidong/判断资讯脚本运行.json'
            self.heimingdan_txt_path = '/www/wwwroot/bcy/qidongdeng_gongju/jiancha_jiaoben_chaoshi/job3_heimingdan.txt'

    def projects(self):  # 获取项目
        r = requests.get(url=self.urls + '/listprojects.json')
        if 'projects' in r.json():
            projects = r.json()['projects']  # ['shishicesi', 'shishizixun']
            for x in projects:
                r1 = requests.get(url=self.urls + '/listspiders.json?project=' + str(x))
                spiders = r1.json()['spiders']
                if 'zixun' in x:
                    for i in spiders:
                        self.zixun_dic[i] = {"yunxing": 1, "biaoqian": x}
                elif 'gongju' in x:
                    for i in spiders:
                        self.gongju_lst[i] = {"yunxing": 1, "biaoqian": x}
                elif 'shishicesi' in x:
                    for i in spiders:
                        self.biaoxun_dic[i] = {"yunxing": 1, "biaoqian": x}
                else:
                    pass

    def qidong(self):
        with open(self.heimingdan_txt_path, 'r', encoding='utf-8') as f:
            job_heimingdan_lst = f.read().split('\n')
        with open(self.zixun_json_path, 'r', encoding='utf-8') as f:
            panduan_zixun_json = json.load(f)
        with open(self.biaoxun_json_path, 'r', encoding='utf-8') as f:
            panduan_biaoxun_json = json.load(f)
        guanjianzi = ['医院', '有限公司', '学院']
        for k1, v1 in panduan_biaoxun_json['jiaoben_dic'].items():
            yunxing_wei0 = True
            guanjianzi_TF = False
            if k1 not in str(job_heimingdan_lst):
                for i in guanjianzi:
                    if i in k1:
                        guanjianzi_TF = True
                        break
                if guanjianzi_TF:
                    if v1['yunxing'] != 0:
                        self.yunxing_jiaoben(k1, v1, panduan_biaoxun_json, self.biaoxun_json_path, yunxing_wei0)
                        time.sleep(1)
                else:
                    yunxing_wei0 = False
                    self.yunxing_jiaoben(k1, v1, panduan_biaoxun_json, self.biaoxun_json_path, yunxing_wei0)
                    time.sleep(1)

        for k1, v1 in panduan_zixun_json['jiaoben_dic'].items():
            yunxing_wei0 = True
            if v1['yunxing'] != 0:
                self.yunxing_jiaoben(k1, v1, panduan_zixun_json, self.zixun_json_path, yunxing_wei0)
                time.sleep(1)

    def yunxing_jiaoben(self, k1, v1, data_json, path, yunxing_wei0):
        while True:
            resp = requests.get(url='{}/listjobs.json'.format(self.urls))
            if len(resp.json()['running']) < 30:
                r = requests.post(url=self.urls + '/schedule.json', data=('project=' + str(v1['biaoqian']) + '&spider=' + str(k1)).encode('utf-8'), headers=self.headers)
                html = r.json()
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if html['status'] == 'ok':
                    print('ok：{}'.format(k1))
                    if yunxing_wei0:
                        data_json['jiaoben_dic'][k1]['yunxing'] = 0
                        with open(path, 'w', encoding='utf-8') as f:
                            json.dump(data_json, f, ensure_ascii=False, indent=4)
                else:
                    print('失败：{}{}{}'.format(k1, html['jobid'], ts))
                break
            else:
                time.sleep(2)

    def meiri_chongzhi_json(self):
        for yuanzu in [(self.zixun_json_path, self.zixun_dic), (self.biaoxun_json_path, self.biaoxun_dic)]:
            with open(yuanzu[0], 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            if json_data['gengxin_time'] != datetime.now().strftime("%Y-%m-%d"):
                json_data['gengxin_time'] = datetime.now().strftime("%Y-%m-%d")
                json_data['jiaoben_dic'] = yuanzu[1]
                with open(yuanzu[0], 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)

    def panduan_wenjian(self):
        for yuanzu in [(self.zixun_json_path, self.zixun_dic), (self.biaoxun_json_path, self.biaoxun_dic)]:
            if not os.path.exists(yuanzu[0]):
                data = {
                    "gengxin_time": datetime.now().strftime("%Y-%m-%d"),
                    "jiaoben_dic": yuanzu[1]
                }
                with open(yuanzu[0], 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    try:
        scrapyd = Scrapyd()
        while True:
            scrapyd.projects()
            scrapyd.panduan_wenjian()
            scrapyd.meiri_chongzhi_json()
            scrapyd.qidong()
            sys.stdout.flush()
    except:
        print(traceback.print_exc())
