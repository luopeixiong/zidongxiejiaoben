import requests
import json


def get_sousuo(dic, cookies, json_data):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'http://caiji.hangxunbao.com',
        'Pragma': 'no-cache',
        'Referer': 'http://caiji.hangxunbao.com/admin/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }

    params = {
        'page': '1',
        'perPage': '20',
        'orderBy': '',
        'orderDir': '',
    }

    items = requests.post(
        'http://caiji.hangxunbao.com/admin/lybiao/list',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    ).json()['data']['items']

    return items


def main(cookies):
    with open('weipa.json', 'r', encoding='utf-8') as f:
        json_list = json.load(f)

    jilu_json_data = {"真未爬": [], "未爬但标签": [], "假未爬": []}
    for dic in json_list:
        json_data = {
            'page': 1,
            'name': '[~]',
            'perPage': 20,
            'url': '[~]{}'.format('/'.join(dic['url'].split('/')[:3])),
            'create_date': '[-]',
            'update_time': '[-]',
        }
        items_url = get_sousuo(dic, cookies, json_data)
        if items_url:  # 如果有此url，说明已经被爬
            print('。。。已爬：' + dic['title'])
            jilu_json_data['假未爬'].append(dic)
            continue
        json_data = {
            'page': 1,
            'name': '[~]{}'.format(dic['title']),
            'perPage': 20,
            'url': '[~]',
            'create_date': '[-]',
            'update_time': '[-]',
        }
        items_name = get_sousuo(dic, cookies, json_data)
        if items_name:  # 如果有此名称，下一步判断url是否有，因为在上面url判断不一定会有
            if dic['url'] in str(items_name):  # 如果url在里面，说明已爬
                print('。。。已爬：' + dic['title'])
                jilu_json_data['假未爬'].append(dic)
                continue
            else:  # 如果url不在里面，说明未爬
                if dic['bz']:  # 如果此未爬有标签注明标签
                    print('？？？未爬但标签：' + dic['title'])
                    jilu_json_data['未爬但标签'].append(dic)
                    continue
                print('！！！未爬：' + dic['title'])
                jilu_json_data['真未爬'].append(dic)
                continue
        else:  # 如果url既没有，也没名称，默认未爬
            if dic['bz']:  # 如果此未爬有标签注明标签
                print('？？？未爬但标签：' + dic['title'])
                jilu_json_data['未爬但标签'].append(dic)
                continue
            print('！！！未爬：' + dic['title'])
            jilu_json_data['真未爬'].append(dic)
            continue

    with open('weipa2.json', 'w', encoding='utf-8') as f:
        json.dump(jilu_json_data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
