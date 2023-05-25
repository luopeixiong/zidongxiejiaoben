import os
import json


json_lst = os.listdir(r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\过滤代理url\baidu_tiaozhuanhou')
big_dic = {}


for josn_name in json_lst:
    print(josn_name)
    # try:
    with open(r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\过滤代理url\baidu_tiaozhuanhou\{}'.format(josn_name), 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 'url_lst_dic' in data.keys():
        for k, url in data['url_lst_dic'].items():
            yuming = url.split('//')[-1].split('/')[0]
            if yuming in big_dic.keys():
                big_dic[yuming] += 1
            else:
                big_dic[yuming] = 1
    # except:
    #     pass
with open(r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\过滤代理url\域名_合并.json', 'r', encoding='utf-8') as f:
    big_dic2 = json.load(f)

sorted_dict = sorted(big_dic.items(), key=lambda x: x[1], reverse=True)
cs_dic = {}
for x in sorted_dict:
    cs_dic[x[0]] = x[1]
with open(r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\过滤代理url\域名_合并.json', 'w', encoding='utf-8') as f:
    json.dump(cs_dic, f, indent=4, ensure_ascii=False)
print('完成')