    def xiayiye_fanye(self, response):
        try:
            qq = '{qianzhui}' + str(int(re.findall(r'{qianzhui}(\d+){houzhui}', response.url)[0]) + 1) + '{houzhui}'
        except:
            qq = '{fanye2_text}'
        if qq and time88(self.zuihou_time):
            qq = qq if 'h' == qq[0] and '/' == qq[6] else response.url.split('/')[0] + '//' + response.url.split('/')[2] + qq if '/' == qq[0] else response.url.replace(response.url.split("/")[-1], "") + qq
            print(qq)
            yield scrapy.Request(qq, callback=self.parse)

