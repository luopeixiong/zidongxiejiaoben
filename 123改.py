import requests
from bs4 import BeautifulSoup
import re
import random
import ddddocr

cookies = {
    'PHPSESSID': 'cfnmivkm1u19slv1js3qah6bhd',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    # 'Cookie': 'PHPSESSID=cfnmivkm1u19slv1js3qah6bhd',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

response = requests.get('http://www.fjchx.com.cn/index/qualification_cert/index', cookies=cookies, headers=headers, verify=False).text

print(response)
# 使用正则表达式匹配包含 name="__token__" 属性的 input 标签
match = re.search(r'<input[^>]*?name="__token__"[^>]*>', response)
token = match.group().split('=')[-1].replace(' />', '').replace('"', '').strip()
print('获取token', token)

headers = {
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': 'PHPSESSID=uhrt3uio05rt59idsifdf958md',
    'Referer': 'http://www.fjchx.com.cn/index/qualification_cert/index',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}
res = requests.get('http://www.fjchx.com.cn/captcha.html', cookies=cookies, headers=headers, verify=False).content
#
with open('./qqqt.jpg', mode='wb')as fils:
    fils.write(res)
#
ocr = ddddocr.DdddOcr()
with open('qqqt.jpg', 'rb') as f:
    img_bytes = f.read()
yzm = ocr.classification(img_bytes)
print('识别出的验证码为：' + yzm)



# 搜索接口
cookies = {
    'PHPSESSID': 'cfnmivkm1u19slv1js3qah6bhd',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://www.fjchx.com.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.fjchx.com.cn/index/qualification_cert/index',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

data = {
    '__token__': token,
    'row[name]': '公司',
    'row[captcha]': yzm,
}

response = requests.post(
    'http://www.fjchx.com.cn/index/qualification_cert/index',
    cookies=cookies,
    headers=headers,
    data=data,
    verify=False,
).json()
print(response)
