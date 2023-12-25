import requests
import json
import guolu_benlai_yipa
import math
import weipa_token


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
        'orderBy': 'bz',
        'orderDir': 'asc',
    }

    json_data = {
        'page': num,
        'hascrawled': False,
        'orderBy': 'bz',
        'orderDir': 'asc',
        'perPage': 100,
        'source': '[~]',
        'url': '[~]',
        'create_date': '[-]',
    }

    response = requests.post(
        'http://caiji.hangxunbao.com/admin/uncrawledsource/list',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    ).json()
    return response['data']['total']


def start(cookies):
    json_data = []
    yuanshi_liebiao = []
    total = req(1, cookies)
    result = math.ceil(total / 100) + 1
    for num in range(1, result):
        print(num)
        response = req(num, cookies)
        for x in response["data"]["items"]:
            yuanzu = x['id'], x['url'], x['source'][::-1], x['bz']
            yuanshi_liebiao.append(yuanzu)
        # time.sleep(5)
    daoxu_liebiao = sorted(yuanshi_liebiao, key=lambda t: t[2], reverse=False)
    for index, url, daoxu_text, bz in daoxu_liebiao:
        json_data.append({'title': daoxu_text[::-1], 'bz': bz, 'url': url})

    with open('weipa.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    print('==============')


def get_access_token():
    json_data = {
        "username": "bichengyi",
        "password": "bichengyi"
    }
    response = requests.post('http://caiji.hangxunbao.com/admin/auth/form/login/api',json=json_data).json()
    return response['data']['access_token']




def main():
    access_token = weipa_token.main()
    cookies = {
        'Authorization': '"bearer %s"' % access_token,
    }
    start(cookies)
    guolu_benlai_yipa.main(cookies)


if __name__ == '__main__':
    main()
