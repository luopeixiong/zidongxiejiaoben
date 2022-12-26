self.zhaozhong_biao(response, items)|
    def zhaozhong_biao(self, response, items):
        for x in {urlpanduan_biaotipanduan}:
            if x in response.url:
                items['channel_id'] = 15  # 中标15  招标16
                break
            else:
                items['channel_id'] = 16  # 中标15  招标16