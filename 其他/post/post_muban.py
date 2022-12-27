# -*- coding: utf-8 -*-
from ..items import *


class {class_name}Spider(scrapy.Spider):
    name = '{py_wenjian_name}'
    items_cource = '{items_cource}'  # 不要加前面数字
    shi = shi()
    allowed_domains = {yuming}
    start_urls = ['{qishi_url}']
    custom_settings = 【
        'DOWNLOAD_DELAY': 0.1,  # 延迟爬取时间，这个就是设置单个爬虫的 settings
        # 'RANDOMIZE_DOWNLOAD_DELAY': True
    】
    headers = 【'Content-Type': 'application/json; charset=UTF-8'】

    mun = 0
    data = {data_list}
    url_pinjie_qianduan = '{url_pingjie_qianduan}'

    # html用。
    {zhengwen_xpath}

    def start_requests(self):  # 首次发送post
        for x in self.data:
            yield scrapy.FormRequest(url=self.start_urls[0], method="POST", headers=self.headers, body=x, callback=self.parse)

    def parse(self, response):
        if response.status == 200 and len(response.text) > 1:
            try:
                rs = json.loads(response.text)
            except:
                rs = response.text
            for x in rs{liebiao_dingwei_text}:
                items = ShishicesiItem()
                titlell = x{liebiao_title_dict_text_lst}
                urlhtml = self.url_pinjie_qianduan + x{liebiao_title_dict_text_lst}
                publishtime = re.findall(r'^(.+?) ', x['syncTime'])[0]
                url = str(urlhtml).replace('&amp;', '&')

                items['publishtime'] = publishtime.replace('.', '-').replace(' ', '').replace('/', '-')
                items['source'] = self.items_cource
                items['notes'] = 'bscrapy'
                items['title'] = titlell
                items['original_url'] = url.replace('&amp;', '&')
                if url and self.shi.shishi(items['source'], str(url)):
                    # 判断招中标
                    {zhaobiao_0}
                    # 爬取列表内各个url的数据
                    yield scrapy.Request(url=url, callback=self.html, meta=【'items': items】)
            # 存在下一页翻页
            yield from self.xiayiye_fanye(response, rs)

    def xiayiye_fanye(self, response, rs):
        page = 'start='  # 需要修改的
        qq = str(response.request.body, 'utf-8') if page in str(response.request.body, 'utf-8') else response.url
        qq = qq.replace(re.findall(r'(' + page + r'\d+)', qq)[0], page + str(int(re.findall(page + r'(\d+)', qq)[0]) + 25))
        if page in str(response.request.body, 'utf-8'):
            yield scrapy.FormRequest(url=response.url, method="POST", body=qq, headers=self.headers, callback=self.parse, dont_filter=True)
        else:
            yield scrapy.FormRequest(qq, callback=self.parse)

    {zhaobiao_1}

    def html(self, response):
        if response.status == 200 and len(response.text) > 10:
            items = response.meta['items']  # 回传管道
            items['title'] = response.xpath(self.zhengwen_title_xpath).extract_first()
            items['content'] = response.xpath(self.zhengwen_content_xpath).extract_first()
            time_text = response.xpath(self.zhengwen_publishtime_xpath).re(self.zhengwen_publishtime_re)
            if time_text:
                items['publishtime'] = time_text[0].replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            self.guding_xieru(response)
            # 如果里面的yield scrapy.Request代码是启动的就用此代码，没有就不用yield from，会报错
            yield from self.guding_xieru(response)

    def guding_xieru(self, response):
        items = response.meta['items']  # 回传管道
        self.shi.shishi1(items['source'], str(response.url))
        if items['title'] is not None and items['content'] is not None:
            if '>' in items['title']:
                items['title'] = re.sub(r'(<(.+?)>)', '', items['title']).strip()
            items['content'] = re.sub(
                r'((href|src)=["|\'])(/(?![/])((?![:]).)+?)(["|\'])',
                r'\g<1>' + response.url.split('/')[0] + '//' + response.url.split('/')[
                    2] + r'\g<3>\g<5>',
                re.sub(
                    r'((href|src)=["|\'])((?![/])((?![:]).)+?)(["|\'])',
                    r'\g<1>' + response.url.replace(
                        response.url.split("/")[-1],
                        ""
                    ) + r'\g<3>\g<5>',
                    items['content']
                )
            )  # 全自动补全升级版
            print(items['channel_id'], len(items['content']), items['publishtime'], items['title'], response.url)  # 输出
            self.shi.shishi1(items['source'],str(response.url))
            yield scrapy.FormRequest(url='http://47.119.131.161/index.php/api/article/crawl',
                                     callback=self.htmliii,
                                     errback=self.err, method="POST", formdata=zidianformdata(items), dont_filter=True)
        else:
            if items['content'] is None and items['title'] is None:
                print('########################################content|title获取不完整： ', response.url)
            elif items['title'] is None:
                print('########################################title获取不完整： ', response.url)
            elif items['content'] is None:
                print('########################################content获取不完整： ', response.url)

    def htmliii(self, response):
        self.mun += 1
        print("------------------------------\n" + response.text)

    def err(self, failure):
        response = failure.value.response
        print("------------------------------\n" + response.text)
