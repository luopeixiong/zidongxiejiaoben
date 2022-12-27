import re


def jichu_data(data_dict):
    bianhao = data_dict['编号'].text()
    zhongwen_ming = data_dict['中文名'].text()
    class_name = data_dict['类名'].text()
    qishi_url_lst = (data_dict['起始url_lst'].toPlainText()).split('\n')
    qishi_url = str(qishi_url_lst)
    yuming = re.findall(r"//(.+?)/", list(qishi_url_lst)[0])
    return bianhao, zhongwen_ming, class_name, qishi_url, yuming


def liebiao_title_url_time(data_dict):
    liebiao_biaoti_xpath = data_dict['列表标题-xpath'].text()  # 如果标题是以文字形式而不是title标签，请在xpath后面加text()，代码需要区分
    liebiao_url_xpath = data_dict['列表url-xpath'].text()

    liebiao_publishtime_xpath = data_dict['列表时间-xpath'].text()  # 使用text()时注意re，re默认启动
    liebiao_publishtime_re = data_dict['列表时间-re'].text()
    liebiao_publishtime_wenjianming = 'liebiao_time1'  # 暂默认不变

    # 列表标题判断
    if 'text()' in liebiao_biaoti_xpath:
        liebiao_biaoti_url_wenjian_name = 'liebiao_title_url2'
    else:
        liebiao_biaoti_url_wenjian_name = 'liebiao_title_url1'
    with open('./getmuban/{}.py'.format(liebiao_biaoti_url_wenjian_name), 'r', encoding='utf8') as f:
        liebiao_biaoti_url_text = f.read()

    liebiao_biaoti_url_text = liebiao_biaoti_url_text.format(title_xpath=liebiao_biaoti_xpath, url_xpath=liebiao_url_xpath)
    liebiao_biaoti_url_text_lst = liebiao_biaoti_url_text.split('~')

    # 列表时间
    with open('./getmuban/{}.py'.format(liebiao_publishtime_wenjianming), 'r', encoding='utf8') as f:
        liebiao_time_text = f.read()
    liebiao_time_text = liebiao_time_text.format(xpath=liebiao_publishtime_xpath, re=liebiao_publishtime_re)
    liebiao_time_lst = liebiao_time_text.split('|')
    return liebiao_biaoti_url_text_lst, liebiao_time_lst


def zhao_zhong_qufen(data_dict):
    zhaobiao_wenjian_name = data_dict['招标方案-文件名'].currentText()  # 暂用2和3，3更新为标题列表形式，其他暂不考虑 1.单个url判断，2和2_2.多个url判断，3.标题判断
    zhaobiao_urlpanduan_biaotipanduan = str(((data_dict['招标url-标题判断'].text()).replace('，', ',')).split(','))
    # 招中标区分
    with open('./getmuban/{}.py'.format(zhaobiao_wenjian_name), 'r', encoding='utf8') as f:
        zhaobiao_text = f.read()

    zhaobiao_text = zhaobiao_text.format(urlpanduan_biaotipanduan=zhaobiao_urlpanduan_biaotipanduan)
    zhaobiao_text_lst = zhaobiao_text.split('|')
    return zhaobiao_text_lst


def fanye(data_dict):
    fanye_wenjian_name = data_dict['翻页方案-文件名'].currentText()
    with open('./getmuban/{}.py'.format(fanye_wenjian_name), 'r', encoding='utf8') as f:
        fanye_text = f.read()
    if fanye_wenjian_name == 'fanye1':
        fanye1_xpath = data_dict['翻页-xpath'].text()
        # 翻页
        fanye_text = fanye_text.format(xpath=fanye1_xpath)
        fanye_text_lst = fanye_text.split('|')
    elif fanye_wenjian_name == 'fanye2':
        fanye2_text = data_dict['翻页2'].text()
        fenge_num = re.findall(r'(\d+)\.', fanye2_text)[0]
        qianzhui = fanye2_text.split('{}.'.format(fenge_num))[0]
        houzhui = '.' + fanye2_text.split('{}.'.format(fenge_num))[1]
        fanye_text = fanye_text.format(
            fanye2_text=fanye2_text,
            qianzhui=qianzhui,
            houzhui=houzhui
        )
        fanye_text_lst = fanye_text.split('|')
    return fanye_text_lst


def zhengwen_title_time_neirong(data_dict):
    zhengwen_title_xpath = data_dict['正文title-xpath'].text()
    zhengwen_publishtime_xpath = data_dict['正文时间-xpath'].text()
    zhengwen_publishtime_re = data_dict['正文时间-re'].text()
    zhengwen_content_xpath = data_dict['正文内容-xpath'].text()
    zhengwen_wenjianjia_name = 'zhengwen_xpath'

    # 正文
    with open('./getmuban/{}.py'.format(zhengwen_wenjianjia_name), 'r', encoding='utf8') as f:
        zhengwen_wenjianjia_name_text = f.read()

    zhengwen_xpath = zhengwen_wenjianjia_name_text.format(
        zhengwen_title_xpath=zhengwen_title_xpath,
        zhengwen_publishtime_xpath=zhengwen_publishtime_xpath,
        zhengwen_publishtime_re=zhengwen_publishtime_re,
        zhengwen_content_xpath=zhengwen_content_xpath
    )
    return zhengwen_xpath


def chuangjian_get(data_dict):
    print(data_dict)

    # 基础数据
    bianhao, zhongwen_ming, class_name, qishi_url, yuming = jichu_data(data_dict)

    # 列表标题，url，时间
    liebiao_biaoti_url_text_lst, liebiao_time_lst = liebiao_title_url_time(data_dict)

    # 翻页
    fanye_text_lst = fanye(data_dict)

    # 招标中标区分
    zhaobiao_text_lst = zhao_zhong_qufen(data_dict)

    # 正文标题，时间，内容
    zhengwen_xpath = zhengwen_title_time_neirong(data_dict)

    with open('get_muban.py', 'r', encoding='utf8') as f:
        get_muban_text = f.read()

    get_muban_text = get_muban_text.format(
        class_name=class_name,
        py_wenjian_name=bianhao + zhongwen_ming,
        items_cource=zhongwen_ming,
        yuming=yuming,
        qishi_url=qishi_url,
        zhaobiao_0=zhaobiao_text_lst[0],
        zhaobiao_1=zhaobiao_text_lst[1],
        fanye_0=fanye_text_lst[0],
        fanye_1=fanye_text_lst[1],
        fanye_2=fanye_text_lst[2],
        zhengwen_xpath=zhengwen_xpath,
        liebiao_title_url_0=liebiao_biaoti_url_text_lst[0],
        liebiao_title_url_1=liebiao_biaoti_url_text_lst[1],
        liebiao_time_0=liebiao_time_lst[0],
        liebiao_time_1=liebiao_time_lst[1]
    )
    get_muban_text = get_muban_text.replace('【', '{').replace('】', '}')
    chuanjian_wenjian_path = r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishicesi\shishicesi\spiders\{}.py'.format(bianhao + zhongwen_ming)
    with open(chuanjian_wenjian_path, 'w', encoding='utf8') as f:
        f.write(get_muban_text)


if __name__ == '__main__':
    pass