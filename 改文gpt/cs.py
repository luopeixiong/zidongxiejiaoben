import json
import uuid
import requests
import random, string
from requests_toolbelt import MultipartEncoder
from pathlib import Path
import os
import re
import time
import math


def shangchuan(headers, mainAccountUid, file_name, sec_token):
    data_params = {
        'Api': 'zeldaEasy.broadscope-bailian.enterprise-data.upload-policy',
        'V': '1.0',
        'Data': {
            'reqDTO': {
                'mainAccountUid': mainAccountUid,
                'fileName': file_name
            },
            'cornerstoneParam': {
                'protocol': 'V2',
                'console': 'ONE_CONSOLE',
                'productCode': 'p_efm',
                'switchAgent': 22928,
                'switchUserType': 3,
                'domain': 'bailian.console.aliyun.com',
                'userNickName': '',
                'userPrincipalName': '',
                'xsp_lang': 'zh-CN'
            }
        }
    }

    data = {
        'params': json.dumps(data_params),
        'region': 'cn-beijing',
        'sec_token': sec_token,
    }

    response = requests.post(
        'https://bailian.console.aliyun.com/data/api.json?action=BroadScopeAspnGateway&product=Beebot-inner&api=zeldaEasy.broadscope-bailian.enterprise-data.upload-policy&_v=5.16.0',
        headers=headers,
        data=data,
    )
    return response


def oss(wenjian_path, shangchuan_json, file_name):
    fields = {
        'OSSAccessKeyId': shangchuan_json['data']['DataV2']['data']['data']['accessId'],
        'policy': shangchuan_json['data']['DataV2']['data']['data']['policy'],
        'signature': shangchuan_json['data']['DataV2']['data']['data']['signature'],
        'key': shangchuan_json['data']['DataV2']['data']['data']['key'],
        'dir': shangchuan_json['data']['DataV2']['data']['data']['dir'],
        'success_action_status': '200',
        'Content_Disposition': 'attachment',
        'file': (file_name, open(wenjian_path, "rb"), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
    }
    boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    m = MultipartEncoder(fields=fields, boundary=boundary)
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'Download Action',
        'Connection': 'keep-alive',
        'Content-Disposition': 'attachment',
        'Content-Type': m.content_type,
        'Origin': 'https://bailian.console.aliyun.com',
        'Pragma': 'no-cache',
        'Referer': 'https://bailian.console.aliyun.com/',
        'Response-type': 'application/json',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    requests.post(url="https://bailian-origin-data.oss-cn-beijing.aliyuncs.com/", headers=headers, data=m)


def tijiao(headers, ossPath, file_name, sec_token):
    data_params = {
        'Api': 'zeldaEasy.broadscope-bailian.enterprise-data.add',
        'V': '1.0',
        'Data': {
            'reqDTO': {
                'dataType': 1,
                'tagIds': [],
                'dataInfos': [{
                    'dataName': file_name,
                    'ossPath': ossPath,
                    'status': 'done',
                    'progress': 1
                }],
                'storeType': 'ES',
                'storeId': 1253
            },
            'cornerstoneParam': {
                'protocol': 'V2',
                'console': 'ONE_CONSOLE',
                'productCode': 'p_efm',
                'switchAgent': 22928,
                'switchUserType': 3,
                'domain': 'bailian.console.aliyun.com',
                'userNickName': '',
                'userPrincipalName': '',
                'xsp_lang': 'zh-CN'
            }
        }
    }

    data = {
        'params': json.dumps(data_params),
        'region': 'cn-beijing',
        'sec_token': sec_token,
    }

    response = requests.post(
        'https://bailian.console.aliyun.com/data/api.json?action=BroadScopeAspnGateway&product=Beebot-inner&api=zeldaEasy.broadscope-bailian.enterprise-data.add&_v=5.16.0',
        headers=headers,
        data=data,
    )
    return response


def main():
    wenjian_path = r"D:\s\测试测试.docx"
    # 文件路径
    file = Path(wenjian_path)
    assert file.exists(), f'不存在文件{file}'
    file_name = wenjian_path.split('\\')[-1]
    cookie = 'currentRegionId=cn-zhangjiakou; cna=zndbHZAt90kCAd7Yo7iapQKm; login_aliyunid_pk=1031035430341318; login_current_pk=1031035430341318; aliyun_lang=zh; _uab_collina=169898760289618543945766; _umdata=G7D63A73CA6088A1CCEAAECD9B509A375B32684; _samesite_flag_=true; cookie2=1682cd042f4ecedd24a4e578cb138b0f; munb=2212848404631; csg=9bcf5c08; t=d685925e3e3dc8bacf40eefaf07391d2; _tb_token_=7f735ee371eb3; login_aliyunid_ticket=1tJw3_1$$aZCpf_8m451v7C1jcp8KIVdUcPu4J1cB2OSmJE9A2xof_BNpwU_TOTNChZBoeM1KJexdfb9zhYnsN5Zos6qISCrRt7mGxbigG2Cd4fWaCmBZHIzsgdZq64XXWQgyKFeuf0vpmV*s*CT58Ml0; login_aliyunid_csrf=_csrf_tk_1832799066054120; hssid=CN-SPLIT-ARCEByIOc2Vzc2lvbl90aWNrZXQyAQE494jqwbkxQAFKEMDNx9jEWbMka4fqXGFANF3aeamSLsXp7y10SbA4jCiFc5J-SQ; hsite=6; aliyun_country=CN; aliyun_site=CN; login_aliyunid_pks=BG+PwXhp5bAi4Qs0LSA6vYe2rutf7Vnl53WYECoxueTD/M=; login_aliyunid=y130****24553; l=fBxm3wtgTyv9WMAFBO5Bnurza779uCAXcsPzaNbMiIEGa6CRxFN6WNCTNUnkIdtjgT5bNexy9EDwTdFySz438tOTC8klTxTCBgpwJe_iYsQ5.; tfstk=dx8Bbaa1eJ2QPCI882GwCrMOEKbSNpgqd71JiQUUwwQdVa9eBBlHaQBWFdOlLalHwaGWLBZF4QHHFU6OJgxFU9W5PQvj_xuquBAhrZHq3qRtNqQjVjJyUKyJtab-3DXHMiOH3E19MGcaUqPZrIM_SPzqFTkcXXfOGF1CXcRFBnKta9sIiBWayxL1QW4VhYl4V5s0P16q1fZuqv_8k2f..; isg=BIeHydl4rlsUOiz9LTAGaIAWFjtRjFtuBF8mT1lwt5Y0yLeKY1_Sv9ROaoiWIDPm'
    sec_token = 'XnKNGXtfFLO7pjf3jojKAE'
    headers = {
        'authority': 'bailian.console.aliyun.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'bx-v': '2.5.3',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
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
    print('写入文件：', wenjian_path)
    mainAccountUid = re.findall('login_aliyunid_pk=(.+?);', cookie)[0]

    response = shangchuan(headers, mainAccountUid, file_name, sec_token)
    if response.status_code == 200:
        print(response.json())
        shangchuan_json = response.json()
        oss(wenjian_path, shangchuan_json, file_name)
        ossPath = shangchuan_json['data']['DataV2']['data']['data']['key']
        response = tijiao(headers, ossPath, file_name, sec_token)
        if response.status_code == 200:
            tijiao_json = response.json()
            print(tijiao_json)
        else:
            print('提交失败')
    else:
        print('上传失败')



if __name__ == '__main__':
    main()




