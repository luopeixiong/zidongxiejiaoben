import requests

headers = {
    'authority': 'cbjtestapi.binjie.site:7777',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://chat1.yqcloud.top',
    'pragma': 'no-cache',
    'referer': 'https://chat1.yqcloud.top/',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

data = '{"prompt":"\u4F60\u662F\u8C01","userId":"#/chat/1683532531024","network":true}'

response = requests.post('https://cbjtestapi.binjie.site:7777/api/generateStream', headers=headers, data=data)
print(response)