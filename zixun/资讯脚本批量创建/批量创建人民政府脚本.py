import pandas as pd
import natsort
import os
import re
import rarfile
import datetime
import shutil
import zipfile


def zip_folder(folder_path, zip_path):
    # 要压缩的文件夹路径

    # 压缩后的zip文件名

    # 创建zip文件对象
    zip_file = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

    # 遍历文件夹及其子文件夹中的文件，并将其写入到zip文件中
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            arc_name = file_path[len(folder_path) + 1:]
            zip_file.write(file_path, arc_name)

    # 关闭zip文件对象
    zip_file.close()


def piliang_chuangjian():
    jiaoben_path = r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\shishicesi\spiders'
    zuixin_biaoqian = 1
    for x in csv_lst:
        data = pd.read_csv(x, encoding='utf-8')

        with open('muban.py', 'r', encoding='utf-8') as f:
            get_muban_text = f.read()
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


def main(csv_lst):
    # 实现备份
    folder_path = r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\shishicesi\spiders'
    now = datetime.datetime.now()
    formatted = now.strftime("%Y_%m_%d_%H_%M_%S")
    zip_path = r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\shishicesi\{}_spidersbf.zip'.format(formatted)
    zip_folder(folder_path, zip_path)

    # 删除spiders文件夹直接删除里面所有的文件
    shutil.rmtree(r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\shishicesi\spiders')

    # 创建spiders文件夹
    os.mkdir(r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\shishicesi\spiders')

    # 创建__init.py__
    f = open(r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\shishicesi\spiders\__init__.py', 'w')
    f.close()

    # 批量创建脚本
    piliang_chuangjian()

    # # 压缩更新后的脚本
    # folder_path = r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\shishicesi\spiders'
    # zip_path = r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\shishicesi\spiders.zip'.format(formatted)
    # zip_folder(folder_path, zip_path)


if __name__ == '__main__':
    csv_lst = ['shengbiao5.csv', 'shi_biao2.csv']
    main(csv_lst)




