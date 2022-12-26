# -*- coding: utf-8 -*-
from ..items import *


class Spider(scrapy.Spider):
    mun = 0
    zuihou_time = None
    shi = shi()

    titlell_xpath = '_标题_xpath_'
    titlell_xpath_re = r"title=[\'|\"](.+?)[\'|\"]"
    urlhtml_xpath = '_url_xpath_'
    publishtime_xpath = '_时间_xpath_'
    publishtime_re = r"_时间_re_"


    def parse(self, response):
        if response.status == 200 and len(response.text) > 1:
            titlell = response.xpath(self.titlell_xpath).extract()
            urlhtml = response.xpath(self.urlhtml_xpath).re(r"href=[\'|\"](.+?)[\'|\"]")
            publishtime = response.xpath(self.publishtime_xpath).re(self.publishtime_re)
            print(len(titlell), len(urlhtml), len(publishtime), response.url)
            for x in range(0, len(urlhtml)):
                items = ShishicesiItem()
                items['publishtime'] = publishtime[x].replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
                self.zuihou_time = items['publishtime']
                # timeStamp = int(time.mktime(time.strptime(items['publishtime'], "%Y-%m-%d %H:%M:%S")))
                # timeStamp = int(time.mktime(time.strptime(items['publishtime'], "%Y-%m-%d")))
                items['source'] = self.items_cource
                items['notes'] = 'bscrapy'
                items['title'] = titlell[x]
                url = str(urlhtml[x]).replace('&amp;', '&')
                url = self.url_pingjie(response, url)
                items['original_url'] = url.replace('&amp;', '&')
                if url and self.shi.shishi(items['source'], str(url)):
                    # 判断招中标
                    self.zhaozhong_biao(response, items)
                    # 爬取列表内各个url的数据
                    yield scrapy.Request(url=url, callback=self.html, meta={'items': items})
            # 存在下一页翻页
            yield from self.xiayiye_fanye(response)


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
            self.shi.shishi1(items['source'], str(response.url))
            yield scrapy.FormRequest(url='http://47.119.131.161/index.php/api/article/crawl', callback=self.htmliii, errback=self.err, method="POST", formdata=zidianformdata(items), dont_filter=True)
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