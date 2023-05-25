import shutil
import os

path = '/www/wwwroot/bcy/gerapy/projects/shishizixun'
dir_lst = os.listdir(path)

for dir_name in dir_lst:
    if 'txt_lst' in dir_name:
        shutil.rmtree('{}/{}'.format(path, dir_name))