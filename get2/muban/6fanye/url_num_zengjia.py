    dierye_pianduan = '{fanye2_text}'
    qianzhui = '{qianzhui}'
    houzhui = '{houzhui}'

~
    def xiayiye_fanye(self, response):
        try:
            qq = self.qianzhui + str(int(re.findall(r'%s(\d+)%s' % (self.qianzhui, self.houzhui), response.url)[0]) + 1) + self.houzhui
        except:
            qq = self.dierye_pianduan
        if qq and time88(self.zuihou_time):
            qq = qq if 'h' == qq[0] and '/' == qq[6] else response.url.split('/')[0] + '//' + response.url.split('/')[2] + qq if '/' == qq[0] else response.url.replace(response.url.split("/")[-1], "") + qq
            print(qq)
            yield scrapy.FormRequest(qq, callback=self.parse)