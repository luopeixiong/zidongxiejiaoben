import os
import re
import time
import requests
import json
from datetime import datetime
import logging
import traceback
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='/www/wwwroot/bcy/qidongdeng_gongju/jiancha_jiaoben_chaoshi/jiancha_jobs3.log',
    level=logging.INFO, filemode='a',
    format='=============================================\n【%(asctime)s】【%(levelname)s】 >>>  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# 定义一个 StreamToLogger 类
class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


# class RiZi:
#     def __init__(self):
#         self.root_path = '/www/wwwroot/bcy/scrapyd/logs/shishicesi'
#         self.dirs_name = os.listdir(self.root_path)
#         self.root_path2 = '/www/wwwroot/bcy/scrapyd/logs/shishizixun'
#         self.dirs_name2 = os.listdir(self.root_path2)
#         self.log_text = ''
#         self.zhongzhi_for = False
#
#         self.baocuo_text = ''
#         self.daimabaocuo_text = ''
#         self.youwu_jinghao = ''
#         self.qitabaocuo_text = ''
#         self.chabudao_meiyouchenggong_str = ''
#
#     def start(self):
#         self.baocuo_text = '=================================以下是存在Traceback报错的日志=========================\n'
#         self.daimabaocuo_text = '=================================以下是存在代码报错的日志=========================\n'
#         self.youwu_jinghao = '=================================以下是存在#######################的日志=========================\n'
#         self.qitabaocuo_text = '=================================以下是存在其他报错的日志=========================\n'
#         self.chabudao_meiyouchenggong_str = '=================================以下是存在chabudao但没有chenggong的日志=========================\n'
#         for dir_name in self.dirs_name:
#             self.zhongzhi_for = False
#             dir_path = '{}/{}'.format(self.root_path, dir_name)
#             dir_duiying_logs_name = os.listdir(dir_path)
#             chuangjiantime_paixu = []
#             for dir_duiying_log_name in dir_duiying_logs_name:
#                 log_path = '{}/{}'.format(dir_path, dir_duiying_log_name)
#                 t = os.path.getmtime(log_path)
#                 timeStruce = time.localtime(t)
#                 times = time.strftime('%Y-%m-%d %H:%M:%S', timeStruce)
#                 chuangjiantime_paixu.append((times, log_path))
#             daoxu_liebiao = sorted(chuangjiantime_paixu, key=lambda t: t[0], reverse=True)
#             for chuangjian_time, log_path in daoxu_liebiao:
#                 with open(log_path, 'r', encoding='utf8') as f:
#                     self.log_text = f.read()
#                 job_time = re.findall(r'(\d\d\d\d\-\d\d\-\d\d \d\d:\d\d:\d\d)', self.log_text)[0]
#                 self.traceback_baocuo(dir_name, job_time, log_path)
#                 self.youwu_jinghao_baocuo(dir_name, job_time, log_path)
#                 if self.zhongzhi_for:
#                     break
#
#     def youwu_jinghao_baocuo(self, dir_name, job_time, log_path):
#         log_url = r'http://192.168.0.233:6800/logs/shishicesi/{}'.format('/'.join(log_path.split('/')[-2:]))
#         if '#######################' in self.log_text:
#             self.youwu_jinghao += '{}--{}：{}\n'.format(dir_name, job_time, log_url)
#             self.zhongzhi_for = True
#
#     def traceback_baocuo(self, dir_name, job_time, log_path):
#         log_url = r'http://192.168.0.233:6800/logs/shishicesi/{}'.format('/'.join(log_path.split('/')[-2:]))
#         if 'Traceback (most recent call last)' in self.log_text:  # 如果这个脚本内的某个脚本的log有Traceback (most recent call last) 脚本必定出
#             if 'shishicesi/spiders' in self.log_text:
#                 # if dir_name not in self.daimabaocuo_text:
#                 self.daimabaocuo_text += '{}--{}：{}\n'.format(dir_name, job_time, log_url)
#                 self.zhongzhi_for = True
#             # elif dir_name not in self.qitabaocuo_text:
#             #     self.qitabaocuo_text += '{}--{}：{}\n'.format(dir_name, job_time, log_url)
#
#     def youwu_jinghao_baocuo2(self, dir_name, job_time, log_path):
#         log_url = r'http://192.168.0.233:6800/logs/shishizixun/{}'.format('/'.join(log_path.split('/')[-2:]))
#         if '#######################' in self.log_text:
#             self.youwu_jinghao += '{}--{}：{}\n'.format(dir_name, job_time, log_url)
#             self.zhongzhi_for = True
#
#     def traceback_baocuo2(self, dir_name, job_time, log_path):
#         log_url = r'http://192.168.0.233:6800/logs/shishizixun/{}'.format('/'.join(log_path.split('/')[-2:]))
#         if 'Traceback (most recent call last)' in self.log_text:  # 如果这个脚本内的某个脚本的log有Traceback (most recent call last) 脚本必定出
#             if 'shishicesi/spiders' in self.log_text:
#                 # if dir_name not in self.daimabaocuo_text:
#                 self.daimabaocuo_text += '{}--{}：{}\n'.format(dir_name, job_time, log_url)
#                 self.zhongzhi_for = True
#             # elif dir_name not in self.qitabaocuo_text:
#             #     self.qitabaocuo_text += '{}--{}：{}\n'.format(dir_name, job_time, log_url)
#
#     def write_txt(self):
#         f = open("/www/wwwroot/bcy/baocuo_log_chazhao.log", "w", encoding='utf8')
#         data_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))  # 获取上次记录的日期和时间
#         f.write('=====================================本次检查时间：{}===================================================\n'.format(data_time))
#         f.write(self.baocuo_text)
#         f.write(self.daimabaocuo_text)
#         f.write(self.youwu_jinghao)
#         f.write(self.chabudao_meiyouchenggong_str)
#         f.write(self.qitabaocuo_text)
#         f.close()
#         print('----完成----')


class ScrapydJobs:
    def __init__(self):
        self.urls = 'http://127.0.0.1:6800'
        self.biaoxun_lst = []
        self.zixun_lst = []
        self.url_liebiao_str = ['shishizixun|0url列表查找']
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        self.heimingdan_txt = open('/www/wwwroot/bcy/qidongdeng_gongju/jiancha_jiaoben_chaoshi/job3_heimingdan.txt', 'a', encoding='utf-8')

    def start(self):
        r = requests.get(url=self.urls + '/listjobs.json')
        if 'running' in str(r.json()):
            running = r.json()['running']
            if running:
                for x in running:
                    qidong_time = str(x['start_time']).split('.')[0]
                    date_obj = datetime.strptime(qidong_time, '%Y-%m-%d %H:%M:%S')
                    # 获取当前时间
                    current_time = datetime.now()
                    # 计算时间差并转换为分钟数
                    time_diff = int(divmod((current_time - date_obj).total_seconds(), 60)[0])
                    if time_diff > 10:
                        self.guanbi_job(x['project'], x['id'], x['spider'])

    def guanbi_job(self, project, i_d, name):
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        r = requests.post(url='http://127.0.0.1:6800' + '/cancel.json', data=('project=' + str(project) + '&job=' + str(i_d)).encode('utf-8'), headers=headers)
        html = r.json()
        if html['status'] == 'ok':
            print('删除超过10分的脚本：{}'.format(name))
            self.heimingdan_txt.write(name + '\n')
            self.heimingdan_txt.flush()


def main():
    try:
        # 创建 logger 实例
        logger = logging.getLogger()
        # 创建 StreamToLogger 实例
        stdout_logger = StreamToLogger(logger, logging.INFO)
        # 将 stdout 重定向到 logger
        sys.stdout = stdout_logger
        sj = ScrapydJobs()
        # r = RiZi()
        while True:
            sj.start()
            # r.start()
            # r.write_txt()
            time.sleep(60 * 5)
    except Exception as e:
        logging.error("主程序抛错：")
        logging.error(e)
        logging.error("\n" + traceback.format_exc())


if __name__ == '__main__':
    main()
