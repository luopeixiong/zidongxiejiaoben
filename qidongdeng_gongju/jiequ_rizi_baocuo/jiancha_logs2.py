import os
import re
import time
import requests
import json
import datetime
import logging
import traceback
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='/www/wwwroot/bcy/qidongdeng_gongju/jiequ_rizi_baocuo/jiancha_logs2.log',
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


class Jobs:
    def __init__(self):
        self.root_path2 = '/www/wwwroot/bcy/scrapyd/logs/shishicesi'
        self.dirs_name2 = os.listdir(self.root_path2)
        self.log_text = ''
        self.zhongzhi_for = False
        self.baocuo_big_dic = {}
        with open('/www/wwwroot/bcy/qidongdeng_gongju/jiequ_rizi_baocuo/jiancha_logs_zhubaocuo2.txt', 'r', encoding='utf-8') as f:
            self.zhubaocuo_lst = f.read().split('\n')

    def start2(self):
        for zhubaocuo in self.zhubaocuo_lst:
            self.baocuo_big_dic[zhubaocuo] = {}
            self.baocuo_big_dic[zhubaocuo]['此报错总数'] = 0
        self.baocuo_big_dic['其他报错'] = {}
        self.baocuo_big_dic['其他报错']['此报错总数'] = 0

        for dir_name in self.dirs_name2:
            self.zhongzhi_for = False
            dir_path = '{}/{}'.format(self.root_path2, dir_name)
            dir_duiying_logs_name = os.listdir(dir_path)
            chuangjiantime_paixu = []
            for dir_duiying_log_name in dir_duiying_logs_name:
                log_path = '{}/{}'.format(dir_path, dir_duiying_log_name)
                t = os.path.getmtime(log_path)
                timeStruce = time.localtime(t)
                times = time.strftime('%Y-%m-%d %H:%M:%S', timeStruce)
                chuangjiantime_paixu.append((times, log_path))
            if chuangjiantime_paixu:
                chuangjian_time, log_path = sorted(chuangjiantime_paixu, key=lambda t: t[0], reverse=True)[0]
                with open(log_path, 'r', encoding='utf8') as f:
                    self.log_text = f.read()
                quanbu_baocuo_lst = re.findall('Traceback(.+?)2023', self.log_text, flags=re.S)
                if quanbu_baocuo_lst:
                    for x in quanbu_baocuo_lst:
                        linshi_lst = x.split(')\n')[::-1]
                        zhu_baocuo_str = ''
                        for y in linshi_lst:
                            if y != '':
                                zhu_baocuo_str = y
                                break
                        txt_wu_cibaocuo = True
                        for zhubaocuo in self.zhubaocuo_lst:  # 这个是txt内的主报错列表
                            if zhubaocuo in zhu_baocuo_str:  # 如果当前报错的主报错在主报错列表内
                                txt_wu_cibaocuo = False
                                self.baocuo_big_dic[zhubaocuo]['此报错总数'] += 1
                                zhu_baocuo_str = zhu_baocuo_str.replace(zhubaocuo, '|')  # 将全部报错的主报错那块替换
                                xiugai_str = x.replace(zhu_baocuo_str, 'File')
                                xiao_baocuo = re.findall('shishicesi/spiders(.+?)File', xiugai_str, flags=re.S)
                                if zhu_baocuo_str not in self.baocuo_big_dic[zhubaocuo].keys():  # 如果当前替换后的报错不在主报错的所有的键内
                                    self.baocuo_big_dic[zhubaocuo][zhu_baocuo_str] = {}
                                    self.baocuo_big_dic[zhubaocuo][zhu_baocuo_str]['内容报错列表'] = xiao_baocuo
                                    self.baocuo_big_dic[zhubaocuo][zhu_baocuo_str]['此报错数量'] = 1
                                    self.baocuo_big_dic[zhubaocuo][zhu_baocuo_str]['有此报错脚本列表'] = [dir_name]
                                else:
                                    self.baocuo_big_dic[zhubaocuo][zhu_baocuo_str]['此报错数量'] += 1
                                    if dir_name not in self.baocuo_big_dic[zhubaocuo][zhu_baocuo_str]['有此报错脚本列表']:
                                        self.baocuo_big_dic[zhubaocuo][zhu_baocuo_str]['内容报错列表'] = xiao_baocuo
                                        self.baocuo_big_dic[zhubaocuo][zhu_baocuo_str]['有此报错脚本列表'].append(dir_name)
                        if txt_wu_cibaocuo:
                            self.baocuo_big_dic['其他报错']['此报错总数'] += 1
                            if zhu_baocuo_str not in self.baocuo_big_dic['其他报错'].keys():
                                xiugai_str = x.replace(zhu_baocuo_str, 'File')
                                xiao_baocuo = re.findall('shishicesi/spiders(.+?)File', xiugai_str, flags=re.S)
                                if zhu_baocuo_str not in self.baocuo_big_dic['其他报错'].keys():  # 如果当前替换后的报错不在主报错的所有的键内
                                    self.baocuo_big_dic['其他报错'][zhu_baocuo_str] = {}
                                    self.baocuo_big_dic['其他报错'][zhu_baocuo_str]['内容报错列表'] = xiao_baocuo
                                    self.baocuo_big_dic['其他报错'][zhu_baocuo_str]['此报错数量'] = 1
                                    self.baocuo_big_dic['其他报错'][zhu_baocuo_str]['有此报错脚本列表'] = [dir_name]
                                else:
                                    self.baocuo_big_dic['其他报错'][zhu_baocuo_str]['此报错数量'] += 1
                                    if dir_name not in self.baocuo_big_dic['其他报错'][zhu_baocuo_str]['有此报错脚本列表']:
                                        self.baocuo_big_dic['其他报错'][zhu_baocuo_str]['内容报错列表'] = xiao_baocuo
                                        self.baocuo_big_dic['其他报错'][zhu_baocuo_str]['有此报错脚本列表'].append(dir_name)

        with open('/www/wwwroot/bcy/qidongdeng_gongju/jiequ_rizi_baocuo/jiancha_logs.json', 'w', encoding='utf-8') as f:
            json.dump(self.baocuo_big_dic, f, indent=4, ensure_ascii=False)

    def start1(self):
        for dir_name in self.dirs_name2:
            self.zhongzhi_for = False
            dir_path = '{}/{}'.format(self.root_path2, dir_name)
            dir_duiying_logs_name = os.listdir(dir_path)
            chuangjiantime_paixu = []
            for dir_duiying_log_name in dir_duiying_logs_name:
                log_path = '{}/{}'.format(dir_path, dir_duiying_log_name)
                t = os.path.getmtime(log_path)
                timeStruce = time.localtime(t)
                times = time.strftime('%Y-%m-%d %H:%M:%S', timeStruce)
                chuangjiantime_paixu.append((times, log_path))
            if chuangjiantime_paixu:
                chuangjian_time, log_path = sorted(chuangjiantime_paixu, key=lambda t: t[0], reverse=True)[0]
                with open(log_path, 'r', encoding='utf8') as f:
                    self.log_text = f.read()
                quanbu_baocuo_lst = re.findall('Traceback(.+?)2023', self.log_text, flags=re.S)
                if quanbu_baocuo_lst:
                    for x in quanbu_baocuo_lst:
                        linshi_lst = x.split('\n')[::-1]
                        zhu_baocuo = None
                        for y in linshi_lst:
                            if y != '':
                                zhu_baocuo = y
                                break
                        baocuo_biaoti = zhu_baocuo.split(':')[0]
                        if baocuo_biaoti not in self.baocuo_big_dic.keys():
                            self.baocuo_big_dic[baocuo_biaoti] = []
                        xiugai_str = x.replace(zhu_baocuo, 'File')
                        xiao_baocuo = re.findall('shishicesi/spiders(.+?)File', xiugai_str, flags=re.S)
                        youci_cuowu = True
                        for z in self.baocuo_big_dic[baocuo_biaoti]:
                            if z['主报错'] == zhu_baocuo:
                                youci_cuowu = False
                                z['内容报错'] = xiao_baocuo
                                z['此报错数量'] += 1
                                if dir_name not in z['有此报错脚本']:
                                    z['有此报错脚本'].append(dir_name)
                        if youci_cuowu:
                            self.baocuo_big_dic[baocuo_biaoti].append({'主报错': zhu_baocuo, '内容报错': xiao_baocuo, '此报错数量': 1, '有此报错脚本': [dir_name]})
        with open('/www/wwwroot/bcy/qidongdeng_gongju/jiequ_rizi_baocuo/jiancha_logs2.json', 'w', encoding='utf-8') as f:
            json.dump(self.baocuo_big_dic, f, indent=4, ensure_ascii=False)


def main():
    try:
        # 创建 logger 实例
        logger = logging.getLogger()
        # 创建 StreamToLogger 实例
        stdout_logger = StreamToLogger(logger, logging.INFO)
        # 将 stdout 重定向到 logger
        sys.stdout = stdout_logger
        j = Jobs()
        j.start2()
        time.sleep(60 * 20)
    except Exception as e:
        logging.error("主程序抛错：")
        logging.error(e)
        logging.error("\n" + traceback.format_exc())



if __name__ == '__main__':
    main()
