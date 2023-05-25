import requests
import json
import guolu_benlai_yipa


def req(num, cookies):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'Authorization="bearer yKYt_T6Tu3LpIm_a1F-a6M7SjV91SrM7TfEW2iS-wUU"',
        'Origin': 'http://caiji.66hangxun.com',
        'Pragma': 'no-cache',
        'Referer': 'http://caiji.66hangxun.com/admin/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    params = {
        'page': str(num),
        'perPage': '100',
        'orderBy': '',
        'orderDir': '',
    }

    json_data = {
        'page': num,
        'hascrawled': False,
        'perPage': 100,
        'create_date': '[-]',
    }

    response = requests.post(
        'http://192.168.0.238/admin/uncrawledsource/list',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    return response


def start(cookies):
    yuanshi_liebiao = []
    for num in range(1, 6):
        print(num)
        response = req(num, cookies)
        rs = json.loads(response.text)
        for x in rs["data"]["items"]:
            if x['bz'] is None:
                yuanzu = x['id'], x['url'], x['source'][::-1], x['bz']
                yuanshi_liebiao.append(yuanzu)
        # time.sleep(5)
    daoxu_liebiao = sorted(yuanshi_liebiao, key=lambda t: t[2], reverse=False)
    f = open('weipa.txt', 'w', encoding='utf8')
    for index, url, daoxu_text, bz in daoxu_liebiao:
        f.write('{}--{}--{}\n'.format(daoxu_text[::-1], bz, url))
    f.close()
    print('==============')


def main():
    cookies = {
        'Authorization': '"bearer tz2xyZUx68QG8zRqZCKU7p3SeMADy5KIPWjPBkRVrlU"',
    }
    start(cookies)
    guolu_benlai_yipa.main(cookies)


if __name__ == '__main__':
    main()
