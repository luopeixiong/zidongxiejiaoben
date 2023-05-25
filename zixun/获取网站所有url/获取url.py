import pandas as pd
import natsort
import os
import re


def main(csv_lst):
    jiaoben_path = r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\shishicesi\spiders'
    for x in csv_lst:
        data = pd.read_csv(x, encoding='utf-8')

        for index, row in data.iterrows():
            if str(row['url']) != 'nan':
                diqu = row['全称'].split(',')
                jiaoben_name = '{}人民政府'.format(''.join(diqu[1:]))


if __name__ == '__main__':
    csv_lst = ['shengbiao5.csv', 'shi_biao2.csv']
    main(csv_lst)