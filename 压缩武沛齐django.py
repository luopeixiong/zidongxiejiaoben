import zipfile
import os
import shutil


def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            # 忽略名为"venv"的文件夹
            if 'venv' in dirs:
                dirs.remove('venv')
            # 忽略名为".idea"的文件夹
            if '.idea' in dirs:
                dirs.remove('.idea')

            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))


def jieya(zip_path, target_path):
    # 打开压缩包
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # 解压全部文件到目标路径
        zip_ref.extractall(target_path)
    print('解压完成。')


def shanchu_wenjian(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.join(directory_path, 'venv') in file_path or os.path.join(directory_path, '.idea') in file_path:
                pass
            else:
                os.remove(file_path)

    for root, dirs, files in os.walk(directory_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if os.path.join(directory_path, 'venv') in dir_path or os.path.join(directory_path, '.idea') in dir_path:
                pass
            else:
                shutil.rmtree(dir_path)


def main():
    jie_or_ya = input('压缩输入1，解压输入2，其他结束：')
    if jie_or_ya == '1':
        bianhao = input('这是第几个视频的代码【如果是第一类第三个请输入1-3】：')
        bianhao = bianhao.replace('-', '_')
        folder_path = 'D:\\pycharm_xiangmu\\wpqDjango\\wpqDjango\\s25\\'
        zip_path = 'D:\\pycharm_xiangmu\\wpqDjango\\wpqDjango\\s25_{}.zip'.format(bianhao)
        zip_folder(folder_path, zip_path)
    elif jie_or_ya == '2':
        # 指定压缩包路径
        path = 'D:\\pycharm_xiangmu\\wpqDjango\\wpqDjango'
        wenjian_name_lst = os.listdir(path)
        for index, x in enumerate(wenjian_name_lst):
            print('{}. {}'.format(index, x))
        xiabiao = int(input('根据上面的下标选择压缩包：'))
        zip_path = '{}\\{}'.format(path, wenjian_name_lst[xiabiao])
        directory_path = 'D:\\pycharm_xiangmu\\wpqDjango\\wpqDjango\\s25'
        shanchu_wenjian(directory_path)
        target_path = 'D:\\pycharm_xiangmu\\wpqDjango\\wpqDjango\\s25\\'
        jieya(zip_path, target_path)


if __name__ == '__main__':
    main()
