    def html(self, response):
        if response.status == 200 and len(response.text) > 10:
            try:
                rs = json.loads(response.text)
            except:
                rs = response.text
            items = response.meta['items']  # 回传管道
            items['title'] = rs{a}
            items['content'] = rs{b}
            time_text = re.findall(r"\d【4】-\d【1,2】-\d【1,2】|\d【4】/\d【1,2】/\d【1,2】|\d【4】.\d【1,2】.\d【1,2】|\d【4】年\d【1,2】月\d【1,2】", str(rs{c}))
            if time_text:
                items['publishtime'] = time_text[0].replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            # self.guding_xieru(response)
            # 如果里面的yield scrapy.Request代码是启动的就用此代码，没有就不用yield from，会报错
            yield from self.guding_xieru(response)