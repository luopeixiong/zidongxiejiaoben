    zhengwen_title_xpath = '{title_xpath}'
    zhengwen_publishtime_xpath = '{time_xpath}'
    zhengwen_publishtime_re = r"{time_re}"
    zhengwen_content_xpath = '{content_xpath}'

~
    def html(self, response):
        if response.status == 200 and len(response.text) > 10:
            items = response.meta['items']  # 回传管道
            items['title'] = response.xpath(self.zhengwen_title_xpath).extract_first()
            items['content'] = response.xpath(self.zhengwen_content_xpath).extract_first()
            time_text = response.xpath(self.zhengwen_publishtime_xpath).re(self.zhengwen_publishtime_re)
            if time_text:
                items['publishtime'] = time_text[0].replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            # self.guding_xieru(response)
            # 如果里面的yield scrapy.Request代码是启动的就用此代码，没有就不用yield from，会报错
            yield from self.guding_xieru(response)

