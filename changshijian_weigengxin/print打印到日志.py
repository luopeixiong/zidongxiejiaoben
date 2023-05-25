# import datetime
# import os
# import time
#
# root_path = os.getcwd() + '/scrapyd/logs/shishicesi'
# dirs_name = os.listdir(root_path)
# for dir_name in dirs_name:
#     dir_path = '{}/{}'.format(root_path, dir_name)
#     dir_duiying_logs_name = os.listdir(dir_path)
#     chuangjiantime_paixu = []
#     for dir_duiying_log_name in dir_duiying_logs_name:
#         log_path = '{}/{}'.format(dir_path, dir_duiying_log_name)
#         t = os.path.getmtime(log_path)
#         timeStruce = time.localtime(t)
#         times = time.strftime('%Y-%m-%d %H:%M:%S', timeStruce)
#         chuangjiantime_paixu.append((times, log_path))
#     daoxu_liebiao = sorted(chuangjiantime_paixu, key=lambda t: t[0], reverse=True)
#     print(daoxu_liebiao)

import logging
import sys


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


# 设置 log 输出到文件
logging.basicConfig(filename='text.log', level=logging.DEBUG)
# 创建 logger 实例
logger = logging.getLogger()
# 创建 StreamToLogger 实例
stdout_logger = StreamToLogger(logger, logging.INFO)
# 将 stdout 重定向到 logger
sys.stdout = stdout_logger

# 使用 print 输出内容
print('123456')
print('2435453345')

