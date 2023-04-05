# -*- coding: utf-8 -*-
from ..items import *


class Spider(scrapy.Spider):
    mun = 0
    zuihou_time = 999
    shi = shi()

    name = ''
    items_cource = ''  # 不要加前面数字
    lei_ming = ''
    headers = {'Content-Type': ''}

    start_urls = []
    allowed_domains = []

    def start_requests(self):  # 首次发送post
        for x in self.start_urls:
            yield scrapy.FormRequest(url=x.split('|')[0], method="POST", headers=self.headers, body=x.split('|')[1], callback=self.parse)

    def parse(self, response, *args, **kwargs):
        if response.status == 200 and len(response.text) > 1:
            try:
                rs = json.loads(response.text)
            except:
                rs = response.text
            for x in rs['']:
                items = ShishicesiItem()
                titlell = x['']
                url = '' + str(x[''])
                publishtime = re.findall(r"\d{4}-\d{1,2}-\d{1,2}|\d{4}/\d{1,2}/\d{1,2}|\d{4}.\d{1,2}.\d{1,2}|\d{4}年\d{1,2}月\d{1,2}", str(x['']))[0]
                # publishtime = time.strftime("%Y-%m-%d", time.localtime(int(str(x{e})[:-3])))
                items['publishtime'] = publishtime.replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
                self.zuihou_time = items['publishtime']
                items['source'] = self.items_cource
                items['notes'] = 'bscrapy'
                items['title'] = titlell
                items['original_url'] = url
                shifouchadao = self.shi.shishi(items['source'], str(url))
                self.logger.info('%s@@@chadedao') if not shifouchadao else self.logger.info('%s@@@chabudao')
                if url and shifouchadao:
                    self.zhaozhong_biao(response, items)
                    # 爬取列表内各个url的数据
                    yield scrapy.Request(url=url, callback=self.html, meta={'items': items})
                    # items['content'] = x['contentdetail']
                    # yield from self.guding_xieru2(response, items)
            # # 存在下一页翻页
            yield from self.xiayiye_fanye(response)

    def zhaozhong_biao(self, response, items):
        if re.findall(r'', response.url)[0] in ['']:  # 中标
            items['channel_id'] = 15  # 中标15  招标16
        else:
            items['channel_id'] = 16  # 中标15  招标16

    def xiayiye_fanye(self, response):
        try:
            old_num = int(re.findall(r'', response.url)[0])
            old_pianduan = r''.replace(r'(\d+)', str(old_num))
            new_num = old_num + int(1)
            new_pianduan = r'&page=(\d+)$'.replace(r'(\d+)', str(new_num))
            qq = (response.url).replace(old_pianduan, new_pianduan)
        except:
            qq = None
        if qq and time88(self.zuihou_time):
            print(qq)
            yield scrapy.Request(qq, callback=self.parse)

    def html(self, response):
        if response.status == 200 and len(response.text) > 10:
            items = response.meta['items']  # 回传管道
            items['title'] = response.xpath('').extract_first()
            items['content'] = response.xpath('').extract_first()
            publishtime = response.xpath('').re(r"\d{4}-\d{1,2}-\d{1,2}|\d{4}/\d{1,2}/\d{1,2}|\d{4}.\d{1,2}.\d{1,2}|\d{4}年\d{1,2}月\d{1,2}")[0]  # r"(\d\d\d\d\-\d\d\-\d\d)"
            items['publishtime'] = publishtime.replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-')
            # if time_text:
            #     items['publishtime'] = time_text[0].replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            # self.guding_xieru(response)
            # 如果里面的yield scrapy.Request代码是启动的就用此代码，没有就不用yield from，会报错
            yield from self.guding_xieru(response)

    def url_pingjie(self, response, url):
        if 'http' == url[:4]:
            url = url
        elif '/' == url[:1]:
            url = '/'.join(response.url.split('/')[:3]) + url  # 删掉res的url到域名位置
        elif './' == url[:2]:
            url = '/'.join(response.url.split('/')[:-1]) + '/' + url.replace('./', '')
        elif '../' in url[:3]:
            daoshu_num = -1 * (url.count('../') + 1)
            url = '/'.join(response.url.split('/')[:daoshu_num]) + '/' + url.replace('../', '')
        else:
            url = '/'.join(response.url.split('/')[:-1]) + '/' + url
        return url

    def guding_xieru(self, response):
        items = response.meta['items']  # 回传管道
        if items['title'] is not None and items['content'] is not None:
            if '>' in items['title']:
                items['title'] = re.sub(r'(<(.+?)>)', '', items['title']).strip()
            items['content'] = re.sub(
                r'((href|src)=["|\'])(/(?![/])((?![:]).)+?)(["|\'])', r'\g<1>' + response.url.split('/')[0] + '//' + response.url.split('/')[2] + r'\g<3>\g<5>', re.sub(
                    r'((href|src)=["|\'])((?![/])((?![:]).)+?)(["|\'])', r'\g<1>' + response.url.replace(
                        response.url.split("/")[-1],
                        ""
                        ) + r'\g<3>\g<5>', items['content']
                    )
                )  # 全自动补全升级版
            print(items['channel_id'], len(items['content']), items['publishtime'], items['title'], items['original_url'])  # 输出
            self.shi.shishi1(items['source'], str(response.url))
            yield scrapy.FormRequest(url='http://192.168.0.238/index.php/api/article/crawl', callback=self.htmliii, errback=self.err, method="POST", formdata=zidianformdata(items), dont_filter=True)
        else:
            if items['content'] is None and items['title'] is None:
                print('########################################content|title获取不完整： ', response.url)
            elif items['title'] is None:
                print('########################################title获取不完整： ', response.url)
            elif items['content'] is None:
                print('########################################content获取不完整： ', response.url)
            self.logger.info('########################################content|titleNo： ', response.url)

    def guding_xieru2(self, response, items):
        if items['title'] is not None and items['content'] is not None:
            if '>' in items['title']:
                items['title'] = re.sub(r'(<(.+?)>)', '', items['title']).strip()
            items['content'] = re.sub(
                r'((href|src)=["|\'])(/(?![/])((?![:]).)+?)(["|\'])', r'\g<1>' + response.url.split('/')[0] + '//' + response.url.split('/')[2] + r'\g<3>\g<5>', re.sub(
                    r'((href|src)=["|\'])((?![/])((?![:]).)+?)(["|\'])', r'\g<1>' + response.url.replace(
                        response.url.split("/")[-1],
                        ""
                    ) + r'\g<3>\g<5>', items['content']
                )
            )  # 全自动补全升级版
            print(items['channel_id'], len(items['content']), items['publishtime'], items['title'], items['original_url'])  # 输出
            self.shi.shishi1(items['source'], str(response.url))
            yield scrapy.FormRequest(url='http://192.168.0.238/index.php/api/article/crawl', callback=self.htmliii, errback=self.err, method="POST", formdata=zidianformdata(items), dont_filter=True)
        else:
            if items['content'] is None and items['title'] is None:
                print('########################################content|title获取不完整： ', response.url)
            elif items['title'] is None:
                print('########################################title获取不完整： ', response.url)
            elif items['content'] is None:
                print('########################################content获取不完整： ', response.url)
            self.logger.info('########################################content|titleNo： ', response.url)

    def htmliii(self, response):
        self.mun += 1
        print("------------------------------\n" + response.text)
        self.logger.info("------------------------------chenggong")

    def err(self, failure):
        response = failure.value.response
        print("------------------------------\n" + response.text)
        self.logger.info("------------------------------shibai")
