def parse(self, response, *args, **kwargs):
    if response.status == 200 and len(response.text) > 1:
        try:
            rs = json.loads(response.text)
        except:
            rs = response.text
        for x in rs['']:
            items = ShishicesiItem()
            titlell = x['']
            urlhtml = x['']
            url = '{a}' + str(urlhtml)
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
                yield scrapy.Request(url=url.replace('&amp;', '&'), callback=self.html, meta={'items': items})
                # yield scrapy.FormRequest(url=url.split('|')[0], method="POST", headers=self.headers, body=url.split('|')[1], callback=self.html, meta={'items': items})
                # items['content'] = x['contentdetail']
                # yield from self.guding_xieru2(response, items)
        # # 存在下一页翻页
        yield from self.xiayiye_fanye(response)

