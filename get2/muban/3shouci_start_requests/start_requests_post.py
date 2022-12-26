    def start_requests(self):  # 首次发送post
        for x in self.data:
            yield scrapy.FormRequest(url=x.split('|')[0], method="POST", body=x.split('|')[0], callback=self.parse)

