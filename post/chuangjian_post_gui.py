import re


def jichu_data(data_dict):
    bianhao = data_dict['编号'].text()
    zhongwen_ming = data_dict['中文名'].text()
    class_name = data_dict['类名'].text()
    qishi_url = data_dict['起始url'].text()
    yuming = re.findall(r"//(.+?)/", qishi_url)
    data_list = (data_dict['起始data_lst'].toPlainText()).split('\n')
    return bianhao, zhongwen_ming, class_name, qishi_url, yuming, data_list


def zhenghe_kuohao(text_lst):
    zhongkuohao_dict_text = '["{}"]'
    zhenghe_zhongkuohao = ''
    for x in range(len(text_lst)):
        hebing = zhongkuohao_dict_text.format(text_lst[x])
        zhenghe_zhongkuohao += hebing
    return zhenghe_zhongkuohao


def dict_title_url_time(data_dict):
    zhenghe_list = []
    liebiao_wanzheng_zhongkuohao_lst = []
    liebiao_dingwei_text_lst = (data_dict['列表定位-dict'].text()).replace('，', ',').split(',')
    zhenghe_list.append(liebiao_dingwei_text_lst)

    liebiao_title_dict_text_lst = data_dict['列表title-dict'].text().replace('，', ',').split(',')
    zhenghe_list.append(liebiao_title_dict_text_lst)

    liebiao_url_dict_text_lst = data_dict['列表url-dict'].text().replace('，', ',').split(',')
    zhenghe_list.append(liebiao_url_dict_text_lst)

    url_pingjie_qianduan = data_dict['列表url-拼接前段'].text()

    liebiao_time_dict_text_lst = data_dict['列表时间-dict'].text().replace('，', ',').split(',')
    zhenghe_list.append(liebiao_time_dict_text_lst)

    time_dict_re_text = data_dict['列表时间-re'].text()

    for text_lst in zhenghe_list:
        zhenghe_zhongkuohao = zhenghe_kuohao(text_lst)
        liebiao_wanzheng_zhongkuohao_lst.append(zhenghe_zhongkuohao)

    return liebiao_wanzheng_zhongkuohao_lst, time_dict_re_text, url_pingjie_qianduan


def zhao_zhong_qufen(data_dict):
    zhaobiao_wenjian_name = data_dict['招标方案-文件名'].currentText()  # 暂用2和3，3更新为标题列表形式，其他暂不考虑 1.单个url判断，2和2_2.多个url判断，3.标题判断
    zhaobiao_urlpanduan_biaotipanduan = str(((data_dict['招标url-标题判断'].text()).replace('，', ',')).split(','))
    # 招中标区分
    with open('./postmuban/{}.py'.format(zhaobiao_wenjian_name), 'r', encoding='utf8') as f:
        zhaobiao_text = f.read()

    zhaobiao_text = zhaobiao_text.format(urlpanduan_biaotipanduan=zhaobiao_urlpanduan_biaotipanduan)
    zhaobiao_text_lst = zhaobiao_text.split('|')
    return zhaobiao_text_lst


def chuangjian_post(data_dict):
    # 基础数据
    bianhao, zhongwen_ming, class_name, qishi_url, yuming, data_list = jichu_data(data_dict)

    liebiao_wanzheng_zhongkuohao_lst, time_dict_re_text, url_pingjie_qianduan = dict_title_url_time(data_dict)

    # 招标中标区分
    zhaobiao_text_lst = zhao_zhong_qufen(data_dict)

    with open('post_muban.py', 'r', encoding='utf8') as f:
        post_muban_text = f.read()

    post_muban_text = post_muban_text.format(
        class_name=class_name,
        py_wenjian_name=bianhao + zhongwen_ming,
        items_cource=zhongwen_ming,
        yuming=yuming,
        qishi_url=qishi_url,
        data_list=data_list,
        liebiao_dingwei_text=liebiao_wanzheng_zhongkuohao_lst[0],
        liebiao_title_dict_text_lst=liebiao_wanzheng_zhongkuohao_lst[1],
        liebiao_url_dict_text_lst=liebiao_wanzheng_zhongkuohao_lst[2],
        url_pingjie_qianduan=url_pingjie_qianduan,
        liebiao_time_dict_text_lst=liebiao_wanzheng_zhongkuohao_lst[3],
        time_dict_re_text=time_dict_re_text,
        zhaobiao_0=zhaobiao_text_lst[0],
        zhaobiao_1=zhaobiao_text_lst[1],
    )
    post_muban_text = post_muban_text.replace('【', '{').replace('】', '}')
    chuanjian_wenjian_path = r'D:\pycharm_xiangmu\shishicesi\gerapy\projects\shishicesi\shishicesi\spiders\{}.py'.format(bianhao + zhongwen_ming)
    with open(chuanjian_wenjian_path, 'w', encoding='utf8') as f:
        f.write(post_muban_text)


if __name__ == '__main__':
    pass
