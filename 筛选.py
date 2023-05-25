import pandas as pd

liebiao = []
data = pd.read_csv(r'D:\pycharm_xiangmu\zidongxiejiaoben\1.csv')
for index, row in data.iterrows():
    liebiao.append(row[0])

with open(r'D:\pycharm_xiangmu\zidongxiejiaoben\广西代理公司.txt', 'r', encoding='utf-8') as f:
    yuan_data_lst = f.read().split('\n')

guolu_lst = []
for x in yuan_data_lst:
    if x not in liebiao:
        guolu_lst.append(x)


f = open(r'D:\pycharm_xiangmu\zidongxiejiaoben\guolu_广西代理公司.txt', 'a', encoding='utf-8')
for x in guolu_lst:
    f.write(x + '\n')