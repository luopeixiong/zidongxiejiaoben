with open('get_muban.py', 'r', encoding='utf8') as f:
    get_muban_text = f.read()

bianhao = '851'
zhongwen_ming = '广东金融学院招与标采购中心'
class_name = 'GuangdongJinrongXueyuan'
yuming = "['bidding.gdufe.edu.cn']"
qishi_url = """[
        'https://cgzx.gduf.edu.cn/cgxx/cggg/xnjzcgl.htm',
        'https://cgzx.gduf.edu.cn/cgxx/cggg/zfjzcgl.htm',
        'https://cgzx.gduf.edu.cn/cgxx/jggg/xnjzcgl.htm',
        'https://cgzx.gduf.edu.cn/cgxx/jggg/zfjzcgl.htm'
    ]
"""
liebiao_biaoti_xpath = '//ul[contains(@class, "ss")]/li/a'  # 如果标题是以文字形式而不是title标签，请在xpath后面加text()，代码需要区分

liebiao_publishtime_xpath = '//ul[contains(@class, "ss")]/li/span'  # 使用text()时注意re，re默认启动
liebiao_publishtime_re = r">(.+?)<"
liebiao_publishtime_wenjianming = 'liebiao_time1'  # 暂默认不变

zhaobiao_wenjian_name = 'zhaobiao2'  # 暂用2和3，3更新为标题列表形式，其他暂不考虑 1.单个url判断，2和2_2.多个url判断，3.标题判断
zhaobiao_urlpanduan_biaotipanduan = "['jggg']"

fanye1_xpath = '//a[contains(text(), "下页")]/@href'
fanye_wenjian_name = 'fanye1'  # 暂默认不变

zhengwen_big_dict = """{
        '0': {
            'zhengwen_url_qianzui_lst': '',
            'zhengwen_title_xpath_lst': '//div[contains(@class, "title")]/h3/text()',
            'zhengwen_publishtime_xpath_lst': '//div[contains(@class, "title")]/div',
            'zhengwen_publishtime_re_lst': r"\]：(.+?)&nbsp;",
            'zhengwen_content_xpath_lst': '//div[contains(@id, "vsb_content")]'
        }
    }
"""

# ※
# chuanjian_wenjian_path = 'chuangjian_cs.py'
chuanjian_wenjian_path = r'D:\pycharm_xiangmu\shishicesi\shishicesi\spiders\{}.py'.format(bianhao+zhongwen_ming)


# 列表标题和url判断
if 'text()' in liebiao_biaoti_xpath:
    liebiao_url_xpath = liebiao_biaoti_xpath.replace('/text()', '')
    liebiao_biaoti_url_wenjian_name = 'liebiao_title_url2'
else:
    liebiao_url_xpath = liebiao_biaoti_xpath
    liebiao_biaoti_url_wenjian_name = 'liebiao_title_url1'
with open('./getmuban/{}.py'.format(liebiao_biaoti_url_wenjian_name), 'r', encoding='utf8') as f:
    liebiao_biaoti_url_text = f.read()

liebiao_biaoti_url_text = liebiao_biaoti_url_text.format(title_xpath=liebiao_biaoti_xpath, url_xpath=liebiao_url_xpath)
liebiao_biaoti_url_text_lst = liebiao_biaoti_url_text.split('~')

# 招中标区分
with open('./getmuban/{}.py'.format(zhaobiao_wenjian_name), 'r', encoding='utf8') as f:
    zhaobiao_text = f.read()

zhaobiao_text = zhaobiao_text.format(urlpanduan_biaotipanduan=zhaobiao_urlpanduan_biaotipanduan)
zhaobiao_text_lst = zhaobiao_text.split('|')

# 翻页
with open('./getmuban/{}.py'.format(fanye_wenjian_name), 'r', encoding='utf8') as f:
    fanye_text = f.read()
fanye_text = fanye_text.format(xpath=fanye1_xpath)
fanye_text_lst = fanye_text.split('|')

# 列表时间
with open('./getmuban/{}.py'.format(liebiao_publishtime_wenjianming), 'r', encoding='utf8') as f:
    liebiao_time_text = f.read()
liebiao_time_text = liebiao_time_text.format(xpath=liebiao_publishtime_xpath, re=liebiao_publishtime_re)
liebiao_time_lst = liebiao_time_text.split('|')


get_muban_text = get_muban_text.format(
    class_name=class_name,
    py_wenjian_name=bianhao+zhongwen_ming,
    items_cource=zhongwen_ming,
    yuming=yuming,
    qishi_url=qishi_url,
    zhaobiao_0=zhaobiao_text_lst[0],
    zhaobiao_1=zhaobiao_text_lst[1],
    fanye_0=fanye_text_lst[0],
    fanye_1=fanye_text_lst[1],
    fanye_2=fanye_text_lst[2],
    zhengwen_big_dict=zhengwen_big_dict,
    liebiao_title_url_0=liebiao_biaoti_url_text_lst[0],
    liebiao_title_url_1=liebiao_biaoti_url_text_lst[1],
    liebiao_time_0=liebiao_time_lst[0],
    liebiao_time_1=liebiao_time_lst[1]
)

get_muban_text = get_muban_text.replace('【', '{').replace('】', '}')
with open(chuanjian_wenjian_path, 'w', encoding='utf8') as f:
    f.write(get_muban_text)
