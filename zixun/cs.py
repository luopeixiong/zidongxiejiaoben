import pandas as pd


# 打开文件
xian_url_txt = open('xian_url_txt.txt', 'a', encoding='utf-8')

# 读取csv文件
data = pd.read_csv('shengbiao5.csv', encoding='utf-8')

# 遍历数据
for index, row in data.iterrows():
    # 判断是否为县级
    if '县' in str(row['全称']) and '县级' not in str(row['全称']):
        # 获取县名
        name = ''.join(str(row['全称']).split(',')[1:])
        print(str(row['全称']))
        # 写入文件
        xian_url_txt.write('{},{}\n'.format(name, str(row['url'])))
        xian_url_txt.flush()