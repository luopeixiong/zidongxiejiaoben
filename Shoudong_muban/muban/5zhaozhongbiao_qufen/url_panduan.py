def zhaozhong_biao(self, response, items):
    if re.findall(r'(.+?)', response.url)[0] in ['']:  # 中标
        items['channel_id'] = 15  # 中标15  招标16
    else:
        items['channel_id'] = 16  # 中标15  招标16

