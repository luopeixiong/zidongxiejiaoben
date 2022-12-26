    if re.findall(r{a}, str(response.url, 'utf-8'))[0] in {b}:  # 中标
        items['channel_id'] = 15  # 中标15  招标16
    else:
        items['channel_id'] = 16  # 中标15  招标16

