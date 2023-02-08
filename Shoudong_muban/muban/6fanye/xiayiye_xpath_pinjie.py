def xiayiye_fanye(self, response):
    try:
        qq = response.xpath('').extract()[0]
    except:
        qq = None
    if qq and time88(self.zuihou_time):
        qq = self.url_pingjie(response, qq)
        yield scrapy.Request(qq, callback=self.parse)

