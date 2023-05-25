from datetime import datetime
import natsort
import time
import requests
import logging
import traceback
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='/www/wwwroot/bcy/zidong_startjob4.log',
    level=logging.DEBUG, filemode='a',
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



class Scrapyd:
    def __init__(self):
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
                else:
                    self.biaoxun_lst = natsort.natsorted(['{}|{}'.format(x, i) for i in spiders])

    def chakan_url_list(self):
        r = requests.get(url=self.urls + '/listjobs.json')
        if 'running' in r.json():
            running = r.json()['running']
            if running:
                if '0url列表' in str(running):
                    pass
                else:
                    r = requests.post(url=self.urls + '/schedule.json', data=('project=' + str(self.url_liebiao_str[0].split('|')[0]) + '&spider=' + str(self.url_liebiao_str[0].split('|')[1])).encode('utf-8'), headers=self.headers)
                    html = r.json()
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if html['status'] == 'ok':
                        print('成功：{}{}{}'.format(self.url_liebiao_str, html['jobid'], ts))
                    else:
                        print('失败：{}{}{}'.format(self.url_liebiao_str, html['jobid'], ts))

    def qidong(self):
        while True:
            self.chakan_url_list()
            sys.stdout.flush()
            time.sleep(10)


def main():
    try:
        # 创建 logger 实例
        logger = logging.getLogger()
        # 创建 StreamToLogger 实例
        stdout_logger = StreamToLogger(logger, logging.INFO)
        # 将 stdout 重定向到 logger
        sys.stdout = stdout_logger
        scrapyd = Scrapyd()
        # scrapyd.projects()
        scrapyd.qidong()
    except Exception as e:
        logging.error("主程序抛错：")
        logging.error(e)
        logging.error("\n" + traceback.format_exc())


if __name__ == '__main__':
    main()
