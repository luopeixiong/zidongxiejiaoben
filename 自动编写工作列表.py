import natsort
import os
import re
from datetime import date
from openpyxl import Workbook
import time


def write_to_excel(data, filename):
    workbook = Workbook()  # 创建一个Workbook对象
    sheet = workbook.active  # 获取当前活动的工作表

    for row in data:
        sheet.append(row)  # 将每行数据添加到工作表

    workbook.save(filename)  # 保存工作表到文件


current_date = date.today()
formatted_date = current_date.strftime("%Y/%m/%d")


def remove_digits(string):
    pattern = r'\d+'  # 匹配一个或多个数字
    result = re.sub(pattern, '', string)  # 使用空字符替换匹配到的数字
    return result


jiaoben_lst = natsort.natsorted(os.listdir(r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishicesi\shishicesi\spiders'))
bianhao = input('请输入今日写的第一个编号【如1895】：')
xiabiao = 0

for index, name in enumerate(jiaoben_lst):
    if bianhao in name:
        xiabiao = index
        break

jinri_jiaoben_list = jiaoben_lst[xiabiao:]
data = []
path = 'D:\\pycharm_xiangmu\\shishicesi\\gerapy\\projects\\shishicesi\\shishicesi\\spiders'

for i in jinri_jiaoben_list:
    # 获取文件的修改时间
    modification_time = os.path.getmtime('{}\\{}'.format(path, i))

    # 将时间戳转换为可读格式
    modification_time_str = time.strftime('%Y/%m/%d', time.localtime(modification_time))
    result = remove_digits(i.replace('.py', ''))
    data.append(['闭城溢', '编写招标网站：{}'.format(result), modification_time_str])

filename = '自动编写工作列表.xlsx'
write_to_excel(data, filename)
print('完成')
