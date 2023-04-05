import pandas as pd


csv_path = 'D:\\pycharm_xiangmu\\zidongxiejiaoben\\zixun'
data = pd.read_csv('{}\\shengbiao4.csv'.format(csv_path), encoding='utf-8')
for index, row in data.iterrows():
    # 访问每一列数据
    i_d = row['ID']
    if str(row['url']) != 'nan':
        if 'http' not in str(row['url']):
            data.loc[data['ID'] == i_d, "url"] = 'http://{}/'.format(str(row['url']))

data.to_csv('{}\\shengbiao5.csv'.format(csv_path), index=False)