def start_requests(self):  # 首次发送post
    for x in self.start_urls:
        yield scrapy.FormRequest(url=x.split('|')[0], method="POST", headers=self.headers, body=x.split('|')[1], callback=self.parse)

