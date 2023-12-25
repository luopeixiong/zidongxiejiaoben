import requests
# from loguru import logger
import base64
import cv2
import execjs


# 加密base64
def base64_encode(input_string):
    # 将输入字符串编码为bytes对象
    bytes_to_encode = input_string.encode('utf-8')

    # 进行Base64加密
    encoded_bytes = base64.b64encode(bytes_to_encode)

    # 将加密后的bytes对象转换为字符串
    encoded_string = encoded_bytes.decode('utf-8')

    return encoded_string


# 识别缺口距离
def getDistance(sliceimgpath, imgpath):
    # 读取背景图片和缺口图片
    bg_img = cv2.imread(imgpath)  # 背景图片
    tp_img = cv2.imread(sliceimgpath)  # 缺口图片

    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)

    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

    # 绘制方框
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite('out.jpg', bg_img)  # 保存在本地
    # 返回缺口距离
    return tl[0]


cookies = {
    'https_waf_cookie': 'ed7a2766-7b22-4b2feece3017be060be5113886d755cafa17',
    'SF_cookie_129': '34440460',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'https_waf_cookie=ed7a2766-7b22-4b2feece3017be060be5113886d755cafa17; SF_cookie_129=34440460',
    'Pragma': 'no-cache',
    'Referer': 'https://xxgs.chinanpo.mca.gov.cn/gsxt/newList',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get(
    'https://xxgs.chinanpo.mca.gov.cn/gsxt/PlatformSHZZFRKGSXT/slideCaptcha',
    cookies=cookies,
    headers=headers,
).json()

# 获得ab值
a = response['result'].get('a', None)
b = response['result'].get('b', None)
qk = response['result']['c'].get('cutImage', None)
bj = response['result']['c'].get('oriImage', None)
print('a值:{}'.format(a))
print('b值:{}'.format(b))
print(qk)
print(bj)

# 2.base64转换为bytes类型
avatar_bytes = base64.b64decode(qk)
# 3.创建一张图片，将bytes类型的数据写入图片中
with open('./1.jpg', 'wb+') as fp:
    fp.write(avatar_bytes)

# 2.base64转换为bytes类型
avatar_bytes2 = base64.b64decode(bj)
# 3.创建一张图片，将bytes类型的数据写入图片中
with open('./2.jpg', 'wb+') as fp:
    fp.write(avatar_bytes2)

sliceimgpath = r'1.jpg'  # 缺口图片
imgpath = r'2.jpg'  # 背景图

# 缺口距离
distans = getDistance(sliceimgpath, imgpath)
print("识别的缺口距离是：{}".format(distans))

# 加密a，b值
new_a = base64_encode(a)
new_b = base64_encode(b)
print('加密的a值:{}'.format(new_a))
print('加密的b值:{}'.format(new_b))
#
with open('123.js', mode='r', encoding='utf-8')as f:
    fitls = f.read()
#
qwe = execjs.compile(fitls)
c = qwe.call("encryptWithRSA", str(distans))

print('得到c值:{}'.format(c))

new_c = base64_encode(c)
print('加密的c值:{}'.format(new_c))

# 测试是否成功通过
cookies = {
    'https_waf_cookie': 'ed7a2766-7b22-4b2feece3017be060be5113886d755cafa17',
    'SF_cookie_129': '34440460',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'https_waf_cookie=ed7a2766-7b22-4b2feece3017be060be5113886d755cafa17; SF_cookie_129=34440460',
    'Pragma': 'no-cache',
    'Referer': 'https://xxgs.chinanpo.mca.gov.cn/gsxt/newList',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'a': f'{new_a}',
    'b': f'{new_b}',
    'c': f'{new_c}',
}

res = requests.get(
    'https://xxgs.chinanpo.mca.gov.cn/gsxt/PlatformSHZZFRKGSXT/slide_captcha_check',
    params=params,
    cookies=cookies,
    headers=headers,
)
print(res.json())
