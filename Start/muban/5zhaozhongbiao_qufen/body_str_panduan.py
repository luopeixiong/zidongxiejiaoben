    def zhaozhong_biao(self, response, items):
        for x in {a}:
            if x in str(response.request.body, 'utf-8'):
                items['channel_id'] = 15  # 中标15  招标16
                break
            else:
                items['channel_id'] = 16  # 中标15  招标16

