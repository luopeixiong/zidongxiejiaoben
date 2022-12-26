# -*- coding: utf-8 -*-
from ..items import *


class Spider(scrapy.Spider):
    mun = 0
    zuihou_time = None
    shi = shi()

{wanzheng_text}


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
            yield scrapy.FormRequest(url='http://192.168.0.238/index.php/api/article/crawl', callback=self.htmliii, errback=self.err, method="POST", formdata=zidianformdata(items), dont_filter=True)
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