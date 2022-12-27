    def xiayiye_fanye(self, response):
        try:
            old_num = int(re.findall(r'{a}', str(response.request.body, 'utf-8'))[0])
            old_pianduan = r'{a}'.replace(r'(\d+)', str(old_num))
            new_num = old_num + 1
            new_pianduan = r'{a}'.replace(r'(\d+)', str(new_num))
            qq = str(response.request.body, 'utf-8').replace(old_pianduan, new_pianduan)
        except:
            qq = None
        if qq and time88(self.zuihou_time):
            print(qq)
            yield scrapy.FormRequest(url=response.url, method="POST", body=qq, callback=self.parse)

