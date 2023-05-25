import shutil
import os

# 遍历指定目录下的所有文件
for filename in os.listdir(r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\url_txt'):
    # 如果文件名符合要求，例如以 .txt 结尾的文件
    if filename.endswith('.txt'):
        # 构造新的文件名，例如在原有文件名前加上“new_”
        newname = '{}人民政府.txt'.format(filename.split('.')[0])
        # 使用shutil模块中的move方法进行重命名
        shutil.move(r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\url_txt\{}'.format(filename), r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishizixun\url_txt\{}'.format(newname))
