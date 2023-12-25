import requests

cookies = {
    't': '4130859ea09285a6cb416a9156e41a6d',
    'currentRegionId': 'cn-zhangjiakou',
    'cna': 'zndbHZAt90kCAd7Yo7iapQKm',
    '_samesite_flag_': 'true',
    'cookie2': '1e6896c9d31f54ff7521465ebca71102',
    '_tb_token_': '56760e55e37ee',
    'login_aliyunid': '"y130****24553"',
    'login_aliyunid_ticket': 'T58JlM_1t$w3C1$_aZ4pfv8m151p7CIjc47KMh48Mx100JjDJlp_X4_Mzpof_BNTwUhTOoNC1ZBeeMfKJzxdnb95hYssNIZor6q7SCxRtgmGCbifG2Cd4ZWazmBdHI6sgXZqg4XFWQfyKpeu*0vCmV*s0',
    'login_aliyunid_csrf': '_csrf_tk_1925098987584046',
    'login_aliyunid_pk': '1031035430341318',
    'login_current_pk': '1031035430341318',
    'login_aliyunid_pks': '"BG+U5uyK/V9H8D7pdSpuBaJY7utf7Vnl53WYECoxueTD/M="',
    'hssid': '43487cab-baba-4f4a-b56e-8d039961b8c2',
    'hsite': '6',
    'aliyun_country': 'CN',
    'aliyun_site': 'CN',
    'aliyun_lang': 'zh',
    '_uab_collina': '169898760289618543945766',
    '_umdata': 'G7D63A73CA6088A1CCEAAECD9B509A375B32684',
    'tfstk': 'du295G0KhwbGS0pT4FChuqv-xtjnBREaAPrWnq0MGyULkrEin5faMWUb8jviIrvY9r4QjhmgmW3YRy3_CA_qHmamJfjam18vHAy3sK0G7xEbrxQlrTXublkrhaboM7As7dk7ox4kIlrZ3xtHl_VQbKePpnIgwOQRZav7F-m1igSngMal8cctPkCyHKsmcU00fHv2nJFK_O7_E8KXzU0-mCsdvIRq1DWI68TO.',
    'l': 'fBxm3wtgTyv9Wk_aBO5Zlurza77OWCRfhsPzaNbMiIEGa6tFgFvbDNCTwC6kzdtjgT5A8eKy9EDwTdhw8Dz_WtOTC8klTxTCB3pM8eM3N7AN.',
    'isg': 'BMDAsFBqscd7B0vojtWp5bNLkU6SSaQT9xIBujpVc1t-tWbf41iBod5DzR11BVzr',
}

headers = {
    'authority': 'bailian.console.aliyun.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'bx-v': '2.5.3',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 't=4130859ea09285a6cb416a9156e41a6d; currentRegionId=cn-zhangjiakou; cna=zndbHZAt90kCAd7Yo7iapQKm; _samesite_flag_=true; cookie2=1e6896c9d31f54ff7521465ebca71102; _tb_token_=56760e55e37ee; login_aliyunid="y130****24553"; login_aliyunid_ticket=T58JlM_1t$w3C1$_aZ4pfv8m151p7CIjc47KMh48Mx100JjDJlp_X4_Mzpof_BNTwUhTOoNC1ZBeeMfKJzxdnb95hYssNIZor6q7SCxRtgmGCbifG2Cd4ZWazmBdHI6sgXZqg4XFWQfyKpeu*0vCmV*s0; login_aliyunid_csrf=_csrf_tk_1925098987584046; login_aliyunid_pk=1031035430341318; login_current_pk=1031035430341318; login_aliyunid_pks="BG+U5uyK/V9H8D7pdSpuBaJY7utf7Vnl53WYECoxueTD/M="; hssid=43487cab-baba-4f4a-b56e-8d039961b8c2; hsite=6; aliyun_country=CN; aliyun_site=CN; aliyun_lang=zh; _uab_collina=169898760289618543945766; _umdata=G7D63A73CA6088A1CCEAAECD9B509A375B32684; tfstk=du295G0KhwbGS0pT4FChuqv-xtjnBREaAPrWnq0MGyULkrEin5faMWUb8jviIrvY9r4QjhmgmW3YRy3_CA_qHmamJfjam18vHAy3sK0G7xEbrxQlrTXublkrhaboM7As7dk7ox4kIlrZ3xtHl_VQbKePpnIgwOQRZav7F-m1igSngMal8cctPkCyHKsmcU00fHv2nJFK_O7_E8KXzU0-mCsdvIRq1DWI68TO.; l=fBxm3wtgTyv9Wk_aBO5Zlurza77OWCRfhsPzaNbMiIEGa6tFgFvbDNCTwC6kzdtjgT5A8eKy9EDwTdhw8Dz_WtOTC8klTxTCB3pM8eM3N7AN.; isg=BMDAsFBqscd7B0vojtWp5bNLkU6SSaQT9xIBujpVc1t-tWbf41iBod5DzR11BVzr',
    'origin': 'https://bailian.console.aliyun.com',
    'pragma': 'no-cache',
    'referer': 'https://bailian.console.aliyun.com/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}

params = {
    'action': 'BroadScopeAspnGateway',
    'product': 'Beebot-inner',
    'api': 'zeldaEasy.broadscope-bailian.enterprise-data.add',
    '_v': '5.16.0',
}

data = {
    'params': '{"Api":"zeldaEasy.broadscope-bailian.enterprise-data.add","V":"1.0","Data":{"reqDTO":{"dataType":1,"tagIds":[],"dataInfos":[{"dataName":"cs.docx","ossPath":"1031035430341318/22928/92a1f5d944db4b86982eb0a2648d080d.1698991380112.docx","status":"done","progress":1}],"storeType":"ES","storeId":1253},"cornerstoneParam":{"protocol":"V2","console":"ONE_CONSOLE","productCode":"p_efm","switchAgent":22928,"switchUserType":3,"domain":"bailian.console.aliyun.com","userNickName":"","userPrincipalName":"","xsp_lang":"zh-CN"}}}',
    'region': 'cn-beijing',
    'sec_token': 'dgzQqtB51AumfP9AyDniD7',
}

response = requests.post(
    'https://bailian.console.aliyun.com/data/api.json',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)