    titlell_xpath = '{title_xpath}'
    titlell_xpath_re = r"title=[\'|\"](.+?)[\'|\"]"
    urlhtml_xpath = '{url_xpath}'
    publishtime_xpath = '{time_xpath}'
    publishtime_re = r"{time_re}"

~
    def parse(self, response, *args, **kwargs):
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

