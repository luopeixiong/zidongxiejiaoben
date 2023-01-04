    def parse(self, response, *args, **kwargs):
        if response.status == 200 and len(response.text) > 1:
            try:
                rs = json.loads(response.text)
            except:
                rs = response.text
            for x in rs{b}:
                items = ShishicesiItem()
                titlell = x{c}
                urlhtml = x{d}
                url = '{a}' + urlhtml
                publishtime = re.findall(r"{f}", str(x{e}))[0]
                items['publishtime'] = publishtime.replace('.', '-').replace(' ', '').replace('/', '-')
                self.zuihou_time = items['publishtime']
                # timeStamp = int(time.mktime(time.strptime(items['publishtime'], "%Y-%m-%d %H:%M:%S")))
                # timeStamp = int(time.mktime(time.strptime(items['publishtime'], "%Y-%m-%d")))
                items['source'] = self.items_cource
                items['notes'] = 'bscrapy'
                items['title'] = titlell
                items['original_url'] = url
                if url and self.shi.shishi(items['source'], str(url)):
                    self.zhaozhong_biao(response, items)
                    # 爬取列表内各个url的数据
                    yield scrapy.Request(url=url.replace('&amp;', '&'), callback=self.html, meta=【'items': items】)
            # # 存在下一页翻页
            yield from self.xiayiye_fanye(response)

