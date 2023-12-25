# -*- coding: utf-8 -*-
from ..items import *


class Spider(scrapy.Spider):
    mun = 0
    zuihou_time = 999
    shi = shi()

{wanzheng_text}


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
        elif '?' == url[:1]:
            url = response.url.split('?')[0] + url
        else:
            url = '/'.join(response.url.split('/')[:-1]) + '/' + url
        return url

    def guding_xieru(self, response):
        items = response.meta['items']  # 回传管道
        if items['title'] is not None and items['content'] is not None:
            if '>' in items['title']:
                items['title'] = re.sub(r'(<(.+?)>)', '', items['title']).strip()
            items['content'] = re.sub(r'((href|src)=["|\'])(/(?![/])((?![:]).)+?)(["|\'])', r'\g<1>' + response.url.split('/')[0] + '//' + response.url.split('/')[2] + r'\g<3>\g<5>', re.sub(r'((href|src)=["|\'])((?![/])((?![:]).)+?)(["|\'])', r'\g<1>' + response.url.replace(response.url.split("/")[-1],
                                                                                                                                                                                                                                                             "") + r'\g<3>\g<5>', items['content']))  # 全自动补全升级版
            print(items['channel_id'], len(items['content']), items['publishtime'], items['title'], items['original_url'])  # 输出
            self.shi.shishi1(items['source'], str(response.url))
            yield scrapy.FormRequest(url='http://192.168.0.228/index.php/api/article/crawl',meta=【'source':str(items['source']),'url':str(response.url)】,callback=self.htmliii,errback=self.err,method="POST",formdata=zidianformdata(items),dont_filter=True)
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
            yield scrapy.FormRequest(url='http://192.168.0.228/index.php/api/article/crawl',meta=【'source':str(items['source']),'url':str(response.url)】,callback=self.htmliii,errback=self.err,method="POST",formdata=zidianformdata(items),dont_filter=True)
        else:
            if items['content'] is None and items['title'] is None:
                print('########################################content|title获取不完整： ', response.url)
            elif items['title'] is None:
                print('########################################title获取不完整： ', response.url)
            elif items['content'] is None:
                print('########################################content获取不完整： ', response.url)
            self.logger.info('########################################content|titleNo： ', response.url)


    def htmliii(self, response):
        self.shi.shishi1(response.meta['source'], response.meta['url'])
        self.mun += 1
        self.logger.info("----------------chenggong--------------\n" + response.text)


    def err(self, failure):
        response = failure.value.response
        self.logger.info("----------------shibai--------------\n" + response.text)