import os
import json
from datetime import datetime

# 格式化时间串
time_str = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
print("当前时间为：", time_str)

num = 2

# 创建文件夹
folder_path = r"D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\过滤代理url\{}_删去大于等于{}".format(time_str, num)  # 文件夹路径
if not os.path.exists(folder_path):  # 判断文件夹是否已经存在
    os.mkdir(folder_path)  # 创建文件夹
    print("文件夹创建成功")
else:
    print("文件夹已经存在")

# 获取域名列表
with open(r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\过滤代理url\域名_合并.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
daishan_yuming_lst = []
for k, v in data.items():
    if v >= num:
        daishan_yuming_lst.append(k)
    elif '.gov.' in k:
        daishan_yuming_lst.append(k)
    elif '.dlzb.' in k:
        daishan_yuming_lst.append(k)
    elif '.zbytb.' in k:
        daishan_yuming_lst.append(k)
    elif '.11467.' in k:
        daishan_yuming_lst.append(k)


json_lst = os.listdir(r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\过滤代理url\baidu_tiaozhuanhou')
big_dic = {}


for josn_name in json_lst:
    try:
        with open(r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\过滤代理url\baidu_tiaozhuanhou\{}'.format(josn_name), 'r', encoding='utf-8') as f:
            data = json.load(f)
        lingshi_k_lst = []
        if 'url_lst_dic' in data.keys():
            if '0' in data['url_lst_dic'].keys():
                for k, url in data['url_lst_dic'].items():
                    if 'www.baidu.com/link?' in url:
                        lingshi_k_lst.append(k)
                    else:
                        yuming = url.split('//')[-1].split('/')[0]
                        if yuming in daishan_yuming_lst:
                            lingshi_k_lst.append(k)
                for k in lingshi_k_lst:
                    del data['url_lst_dic'][k]
                youlianjie = False
                for x in data['url_lst_dic']:
                    youlianjie = True
                    break
                if youlianjie:
                    print(josn_name)
                    with open(r'{}\{}'.format(folder_path, josn_name), 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
    except:
        pass