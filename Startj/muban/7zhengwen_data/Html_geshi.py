    def html(self, response):
        if response.status == 200 and len(response.text) > 10:
            items = response.meta['items']  # 回传管道
            items['title'] = response.xpath('{title_xpath}').extract_first()
            items['content'] = response.xpath('{content_xpath}').extract_first()
            publishtime = response.xpath('{time_xpath}').re(r"\d【4】-\d【1,2】-\d【1,2】|\d【4】/\d【1,2】/\d【1,2】|\d【4】.\d【1,2】.\d【1,2】|\d【4】年\d【1,2】月\d【1,2】")[0]  # r"{time_re}"
            items['publishtime'] = publishtime.replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-')
            # if time_text:
            #     items['publishtime'] = time_text[0].replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            # self.guding_xieru(response)
            # 如果里面的yield scrapy.Request代码是启动的就用此代码，没有就不用yield from，会报错
            yield from self.guding_xieru(response)

