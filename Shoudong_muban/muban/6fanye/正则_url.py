def xiayiye_fanye(self, response):
    try:
        old_num = int(re.findall(r'&page=(\d+)', str(response.url))[0])
        old_pianduan = r'&page=(\d+)'.replace(r'(\d+)', str(old_num))
        new_num = old_num + int(1)
        new_pianduan = r'&page=(\d+)'.replace(r'(\d+)', str(new_num))
        qq = str(response.url).replace(old_pianduan, new_pianduan)
    except:
        qq = None
    if qq and time88(self.zuihou_time):
        print(qq)
        yield scrapy.Request(qq, callback=self.parse)
def xiayiye_fanye(self, response):
    try:
        old_num = int(re.findall(r'{a}', response.url)[0])
        old_pianduan = r'{a}'.replace(r'(\d+)', str(old_num))
        new_num = old_num + int({b})
        new_pianduan = r'{a}'.replace(r'(\d+)', str(new_num))
        qq = (response.url).replace(old_pianduan, new_pianduan)
    except:
        qq = None
    if qq and time88(self.zuihou_time):
        print(qq)
        yield scrapy.Request(qq, callback=self.parse)

