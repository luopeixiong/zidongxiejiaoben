import os
import natsort
import re
import json


def chuangjian_json_file(jiaoben_name):
    with open('json_dir\\{}.json'.format(jiaoben_name), 'w', encoding='utf-8') as f:
        f.write('{}')
    with open('json_dir\\{}.json'.format(jiaoben_name), 'r', encoding='utf-8') as f:
        json_file = json.load(f)
    return json_file


def main():
    json_dir_name = 'json_dir'
    if not os.path.exists(json_dir_name):
        os.makedirs(json_dir_name)
    path = 'txt_dir'
    dir_lst = os.listdir(path)
    dir_path_lst = ['{}\\{}'.format(path, dir_name) for dir_name in dir_lst]
    liebiao_txt_path_lst = []
    for x in dir_path_lst:
        txt_lst = os.listdir(x)
        for i in txt_lst:
            if '_liebiao.' in i:
                liebiao_txt_path_lst.append('{}\\{}'.format(x, i))

    for txt_path in natsort.natsorted(liebiao_txt_path_lst):
        jiaoben_name = re.findall('\\\(.+?)_', txt_path)[1]
        json_file = chuangjian_json_file(jiaoben_name)
        url_mowei_xiegang = {}
        url_indexstr = {}
        url_liststr = {}
        url_qita = []
        with open(txt_path, 'r', encoding='utf-8') as f:
            url_siweitime_erweitime_str_lst = f.read().split('\n')
        for url_siweitime_erweitime_str in url_siweitime_erweitime_str_lst:
            if url_siweitime_erweitime_str != '':
                url, siwei_time, erwei_time = url_siweitime_erweitime_str.split(',')
                siweitime_erweitime_str = '{}_{}'.format(siwei_time, erwei_time)
                if url[-1] == '/':
                    if siweitime_erweitime_str not in url_mowei_xiegang.keys():
                        url_mowei_xiegang[siweitime_erweitime_str] = []
                        url_mowei_xiegang[siweitime_erweitime_str].append(url)
                    else:
                        url_mowei_xiegang[siweitime_erweitime_str].append(url)
                elif 'index' in url.split('/')[-1]:
                    if siweitime_erweitime_str not in url_indexstr.keys():
                        url_indexstr[siweitime_erweitime_str] = []
                        url_indexstr[siweitime_erweitime_str].append(url)
                    else:
                        url_indexstr[siweitime_erweitime_str].append(url)
                elif 'list' in url.split('/')[-1]:
                    if siweitime_erweitime_str not in url_liststr.keys():
                        url_liststr[siweitime_erweitime_str] = []
                        url_liststr[siweitime_erweitime_str].append(url)
                    else:
                        url_liststr[siweitime_erweitime_str].append(url)
                else:
                    url_qita.append(url)
            # qita_url排序
            url_qita = sorted(url_qita, key=lambda i: len(i), reverse=False)
        print('完成：{}'.format(jiaoben_name))
        json_file['url_mowei_xiegang'] = url_mowei_xiegang
        json_file['url_indexstr'] = url_indexstr
        json_file['url_liststr'] = url_liststr
        json_file['url_qita'] = url_qita
        with open('json_dir\\{}.json'.format(jiaoben_name), 'w', encoding='utf-8') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
