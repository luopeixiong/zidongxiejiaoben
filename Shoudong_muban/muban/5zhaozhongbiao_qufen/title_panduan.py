def zhaozhong_biao(self, response, items):
    for x in ['']:
        if x in items['title']:
            items['channel_id'] = 15  # 中标15  招标16
            break
        else:
            items['channel_id'] = 16  # 中标15  招标16

