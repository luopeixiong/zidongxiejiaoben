import pandas as pd
import natsort
import os
import re

jiaoben_path = r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\shishicesi\spiders'
zuixin_biaoqian = int(re.findall(r'(\d+)', natsort.natsorted(os.listdir(jiaoben_path))[-3])[0]) + 1


# 3062
for x in ['shengbiao5.csv', 'shi_biao2.csv']:
    data = pd.read_csv(x, encoding='utf-8')

    with open('muban.py', 'r', encoding='utf-8') as f:
        get_muban_text = f.read()
    # TODO:创建脚本
    for index, row in data.iterrows():
        if str(row['url']) != 'nan':
            diqu = row['全称'].split(',')
            jiaoben_name = '{}{}人民政府'.format(zuixin_biaoqian, ''.join(diqu[1:]))
            if '//' in str(row['url']):
                yuming = str(row['url']).split('/')[2]
            else:
                yuming = str(row['url'])

            get_muban_gaihao_text = get_muban_text.format(
                num_zhongwen=jiaoben_name,
                zhongwen=str(''.join(diqu[1:])) + '人民政府',
                url=str(row['url']),
                yuming=yuming
            )
            get_muban_gaihao_text = get_muban_gaihao_text.replace('【', '{').replace('】', '}')
            print('{}\{}.py'.format(jiaoben_path, jiaoben_name))
            chuanjian_wenjian_path = r'{}\{}.py'.format(jiaoben_path, jiaoben_name)
            with open(chuanjian_wenjian_path, 'w', encoding='utf8') as f:
                f.write(get_muban_gaihao_text)
            zuixin_biaoqian += 1
