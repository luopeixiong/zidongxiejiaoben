self.zhaozhong_biao(response, items)|
    def zhaozhong_biao(self, response, items):
        if 'zbgg1' in response.url:
            items['channel_id'] = 15  # 中标15  招标16
        else:
            items['channel_id'] = 16  # 中标15  招标16