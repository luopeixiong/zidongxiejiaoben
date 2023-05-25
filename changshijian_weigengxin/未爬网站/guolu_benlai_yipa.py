import requests
import json


def get_sousuo(name, cookies):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'Authorization="bearer 9PFRXnsBfeQVRN3F6s55IdOeQr2bMhwyeLVKvl8iX5Y"',
        'Origin': 'http://192.168.0.238',
        'Pragma': 'no-cache',
        'Referer': 'http://192.168.0.238/admin/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }

    params = {
        'page': '1',
        'perPage': '20',
        'orderBy': '',
        'orderDir': '',
    }

    json_data = {
        'page': 1,
        'name': '[~]{}'.format(name),
        'perPage': 20,
        'url': '[~]',
        'create_date': '[-]',
        'update_time': '[-]',
    }

    items = requests.post(
        'http://192.168.0.238/admin/lybiao/list',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    ).json()['data']['items']

    return items


def main(cookies):
    with open('weipa.txt', 'r', encoding='utf-8') as f:
        data_lst = f.read().split('\n')

    zhen_weipa_lst = []
    jia_wei_pa_lst = []
    for x in data_lst:
        name = x.split('--')[0]
        print(name)
        items = get_sousuo(name, cookies)
        if not items:
            zhen_weipa_lst.append(x)
        else:
            jia_wei_pa_lst.append(x)

    f = open('zhen_weipa.txt', 'w', encoding='utf8')
    for i in zhen_weipa_lst:
        f.write('{}\n'.format(i))
    f.close()
    f = open('jia_weipa.txt', 'w', encoding='utf8')
    for i in jia_wei_pa_lst:
        f.write('{}\n'.format(i))
    f.close()


if __name__ == '__main__':
    main()
