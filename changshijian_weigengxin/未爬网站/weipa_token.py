import requests


def get_access_token():
    json_data = {
        "username": "bichengyi",
        "password": "bichengyi"
    }
    response = requests.post('http://caiji.hangxunbao.com/admin/auth/form/login/api', json=json_data).json()
    return response['data']['access_token']


def get_total(num, cookies):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'Authorization="bearer {}"'.format(cookies),
        'Origin': 'http://caiji.66hangxun.com',
        'Pragma': 'no-cache',
        'Referer': 'http://caiji.66hangxun.com/admin/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    params = {
        'page': str(num),
        'perPage': '10',
        'orderBy': 'bz',
        'orderDir': 'asc',
    }

    json_data = {
        'page': num,
        'hascrawled': False,
        'orderBy': 'bz',
        'orderDir': 'asc',
        'perPage': 10,
        'source': '[~]',
        'url': '[~]',
        'create_date': '[-]',
    }

    response = requests.post(
        'http://caiji.hangxunbao.com/admin/uncrawledsource/list',
        params=params,
        headers=headers,
        json=json_data,
        verify=False,
    ).json()['data']['total']
    return response


def main():
    with open('token.txt', 'r') as f:
        access_token = f.read()
    try:
        total = get_total(1, access_token)
        print('token可用')
    except:
        print('token失效，重置token')
        access_token = get_access_token()
        with open('token.txt', 'w') as f:
            f.write(access_token)
    with open('token.txt', 'r') as f:
        access_token = f.read()
    return access_token


if __name__ == '__main__':
    main()
