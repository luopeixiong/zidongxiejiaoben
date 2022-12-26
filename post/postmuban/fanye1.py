xiayiye_xpath = '{xpath}'|yield from self.xiayiye_fanye(response)|
    def xiayiye_fanye(self, response):
        try:
            qq = response.xpath(self.xiayiye_xpath).extract()[0]
        except:
            qq = None
        if qq and time88(self.zuihou_time):
            qq = qq if 'h' == qq[0] and '/' == qq[6] else response.url.split('/')[0] + '//' + \
                                                          response.url.split('/')[2] + qq if '/' == qq[
                0] else response.url.replace(response.url.split("/")[-1], "") + qq
            yield scrapy.Request(qq, callback=self.parse)