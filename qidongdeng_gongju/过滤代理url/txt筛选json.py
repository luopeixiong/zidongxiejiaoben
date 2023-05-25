import os



with open(r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\过滤代理url\aiqicha_agencyuncrawledsource.txt', 'r', encoding='utf-8') as f:
    txt_data = f.read().split('\n')


json_data = os.listdir(r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\过滤代理url\2023_05_12_16_37_51_删去大于等于2')


for x in txt_data:
    name = x.split(',')[1]
    for i in json_data:
        if name in i:
            try:
                os.remove(r'D:\pycharm_xiangmu\zidongxiejiaoben\qidongdeng_gongju\过滤代理url\2023_05_12_16_37_51_删去大于等于2\{}'.format(i))
            except:
                print('报错')
            break
