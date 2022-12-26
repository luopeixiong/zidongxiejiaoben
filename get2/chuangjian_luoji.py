import re


def jichu_data(data_dict, wanzheng_text):
    wenjianming = ''
    for k, v in data_dict.items():
        if '_基础数据_' in k:
            with open('./muban/1kaitou/{}.py'.format('kaitou1'), 'r', encoding='utf8') as f:
                wenjianming = v[0].text()+v[1].text()
                text = f.read().format(a=(v[0].text()+v[1].text()), b=v[1].text(), c=v[2].text())
                wanzheng_text += text
    return wanzheng_text, wenjianming


def start_urldata(data_dict, wanzheng_text):
    zhaobiao_url_lst = []
    zhongbiao_url_lst = []
    for k, v in data_dict.items():
        if '_start_urlAnddata_' in k:
            if "_无_" in k:
                zhaobiao_url_lst += (v[0].toPlainText()).split('\n')
                zhongbiao_url_lst += (v[1].toPlainText()).split('\n')
            elif "_查询字符串参数_" in k:
                zhaobiao_daipinjie_data_lst = (v[1].toPlainText()).split('\n')
                for data in zhaobiao_daipinjie_data_lst:
                    zhaobiao_url_lst.append('{}?{}'.format(v[0].text(), data))
                zhongbiao_daipinjie_data_lst = (v[2].toPlainText()).split('\n')
                for data in zhongbiao_daipinjie_data_lst:
                    zhongbiao_url_lst.append('{}?{}'.format(v[0].text(), data))
            elif "_表单数据_" in k:
                zhaobiao_daipinjie_data_lst = (v[1].toPlainText()).split('\n')
                for data in zhaobiao_daipinjie_data_lst:
                    zhaobiao_url_lst.append('{}|{}'.format(v[0].text(), data))
                zhongbiao_daipinjie_data_lst = (v[2].toPlainText()).split('\n')
                for data in zhongbiao_daipinjie_data_lst:
                    zhongbiao_url_lst.append('{}|{}'.format(v[0].text(), data))

            with open('./muban/2start_urldata/{}.py'.format('1'), 'r', encoding='utf8') as f:
                text = f.read()
            wanzheng_text += text.format(a=str(zhaobiao_url_lst)+str(zhongbiao_url_lst))
    return wanzheng_text


def start_requests_luoji(data_dict, wanzheng_text):
    for k, v in data_dict.items():
        if '_start_requests_' in k:
            a = v[0].currentText()
            if "_GET_" in a:
                with open('./muban/3shouci_start_requests/{}.py'.format('start_requests_get'), 'r', encoding='utf8') as f:
                    text = f.read()
                    wanzheng_text += text
            elif "_POST_" in a:
                with open('./muban/3shouci_start_requests/{}.py'.format('start_requests_post'), 'r', encoding='utf8') as f:
                    text = f.read()
                    wanzheng_text += text
    return wanzheng_text


def liebiao_data(data_dict, wanzheng_text):
    for k, v in data_dict.items():
        if '_列表页面_' in k:
            if "_Html格式_" in k:
                with open('./muban/4liebiao_data/{}.py'.format('html_geshi'), 'r', encoding='utf8') as f:
                    text_lst = f.read().split('~')
                    qianduan_text = text_lst[0].format(title_xpath=v[0].text(), url_xpath=v[1].text(), time_xpath=v[2].text(), time_re=v[3].text())
                    houduan_text = text_lst[1]
                    wanzheng_text = qianduan_text + wanzheng_text
                    wanzheng_text = wanzheng_text + houduan_text
            elif '_Json包_' in k:
                with open('./muban/4liebiao_data/{}.py'.format('json_bao'), 'r', encoding='utf8') as f:
                    bugen_text_lst = f.read().split('~')
                    wanzheng_text = bugen_text_lst[0] + wanzheng_text
                    wanzheng_text = wanzheng_text + bugen_text_lst[1]
    return wanzheng_text


def zhaozhongbiao_qufen(data_dict, wanzheng_text):
    for k, v in data_dict.items():
        if '_招中标区分_' in k:
            if "_标题判断_" in k:
                with open('./muban/5zhaozhongbiao_qufen/{}.py'.format('title_panduan'), 'r', encoding='utf8') as f:
                    text = f.read()
            elif "_url判断_" in k:
                with open('./muban/5zhaozhongbiao_qufen/{}.py'.format('url_panduan'), 'r', encoding='utf8') as f:
                    text = f.read()
            elif "_body判断_" in k:
                with open('./muban/5zhaozhongbiao_qufen/{}.py'.format('body_panduan'), 'r', encoding='utf8') as f:
                    text = f.read()
            text = text.format(a=str((v[0].toPlainText()).split('\n')))
            wanzheng_text += text
    return wanzheng_text


def fanye(data_dict, wanzheng_text):
    for k, v in data_dict.items():
        if '_翻页_' in k:
            if "_下一页xpath_" in k:
                with open('./muban/6fanye/{}.py'.format('xiayiye_xpath_pinjie'), 'r', encoding='utf8') as f:
                    bugen_text_lst = f.read().split('~')
                    wanzheng_text = bugen_text_lst[0].format(xpath=v[0].text()) + wanzheng_text
                    wanzheng_text = wanzheng_text + bugen_text_lst[1]
            elif '_url_num增加_' in k:
                with open('./muban/6fanye/{}.py'.format('url_num_zengjia'), 'r', encoding='utf8') as f:
                    bugen_text_lst = f.read().split('~')
                    fenge_num = re.findall(r'(\d+)\.', v[0].text())[0]
                    qianzhui = v[0].text().split('{}.'.format(fenge_num))[0]
                    houzhui = '.' + v[0].text().split('{}.'.format(fenge_num))[1]
                    wanzheng_text = bugen_text_lst[0].format(fanye2_text=v[0].text(), qianzhui=qianzhui, houzhui=houzhui) + wanzheng_text
                    wanzheng_text = wanzheng_text + bugen_text_lst[1]
    return wanzheng_text


def xiangxiye(data_dict, wanzheng_text):
    for k, v in data_dict.items():
        if '_详细页_' in k:
            with open('./muban/7zhengwen_data/{}.py'.format('Html_geshi'), 'r', encoding='utf8') as f:
                text_lst = f.read().split('~')
                qianduan = text_lst[0].format(title_xpath=v[0].text(), time_xpath=v[1].text(), time_re=v[2].text(), content_xpath=v[3].text())
                wanzheng_text = qianduan + wanzheng_text
                wanzheng_text += text_lst[1]
    return wanzheng_text


def chuangjian(data_dict):
    # print(data_dict)
    wanzheng_text = ''
    wenjianming = ''

    # 基础数据
    if re.findall(r'\'(\d+)_基础数据_', str(data_dict)):
        wanzheng_text, wenjianming = jichu_data(data_dict, wanzheng_text)

    if re.findall(r'\'(\d+)_start_urlAnddata_', str(data_dict)):
        wanzheng_text = start_urldata(data_dict, wanzheng_text)

    # 第一次start_requests以及对应的url和data

    if re.findall(r'\'(\d+)_start_requests_', str(data_dict)):
        wanzheng_text = start_requests_luoji(data_dict, wanzheng_text)

    # 列表标题，url，时间
    if re.findall(r'\'(\d+)_列表页面_', str(data_dict)):
        wanzheng_text = liebiao_data(data_dict, wanzheng_text)

    # 招标中标区分
    if re.findall(r'\'(\d+)_招中标区分_', str(data_dict)):
        wanzheng_text = zhaozhongbiao_qufen(data_dict, wanzheng_text)

    # 翻页
    if re.findall(r'\'(\d+)_翻页_', str(data_dict)):
        wanzheng_text = fanye(data_dict, wanzheng_text)
    #
    # # 正文标题，时间，内容
    if re.findall(r'\'(\d+)_详细页_', str(data_dict)):
        wanzheng_text = xiangxiye(data_dict, wanzheng_text)

    with open('jiben_kuangjia.py', 'r', encoding='utf8') as f:
        get_muban_text = f.read()

    get_muban_text = get_muban_text.format(wanzheng_text=wanzheng_text)
    get_muban_text = get_muban_text.replace('【', '{').replace('】', '}')
    chuanjian_wenjian_path = r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishicesi\shishicesi\spiders\{}.py'.format(wenjianming)
    with open(chuanjian_wenjian_path, 'w', encoding='utf8') as f:
        f.write(get_muban_text)


if __name__ == '__main__':
    pass