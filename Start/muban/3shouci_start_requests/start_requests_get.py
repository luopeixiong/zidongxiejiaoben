    def start_requests(self):  # 首次发送get
        for x in self.start_urls:
            yield scrapy.Request(url=x, callback=self.parse)

