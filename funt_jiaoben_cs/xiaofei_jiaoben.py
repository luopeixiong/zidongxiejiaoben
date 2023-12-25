import requests
from fake_useragent import UserAgent
from funboost import boost, BrokerEnum

ua = UserAgent()
session = requests.Session()


@boost('liebiaoye_qingqiu_name', log_level=20, is_using_rpc_mode=True, broker_kind=BrokerEnum.REDIS, max_retry_times=1)
def liebiaoye_qingqiu(url, items):
    headers = {'User-Agent': ua.Chrome}
    try:
        html_text = session.get(url, headers=headers, timeout=10, verify=False).content.decode('utf-8')
    except:
        html_text = None
    return {'html_text': html_text, 'items': items}


@boost('neirongye_qingqiu_name', log_level=20, is_using_rpc_mode=True, broker_kind=BrokerEnum.REDIS, max_retry_times=1)
def neirongye_qingqiu(url, data):
    headers = {'User-Agent': ua.Chrome}
    try:
        html_text = session.get(url, headers=headers, timeout=10, verify=False).content.decode('utf-8')
    except:
        html_text = None
    return {'html_text': html_text, 'items': data}


@boost('crawl_qingqiu_name', log_level=20, is_using_rpc_mode=True, broker_kind=BrokerEnum.REDIS, max_retry_times=1)
def crawl_qingqiu(data):
    try:
        html_text = session.post('http://192.168.0.228/index.php/api/article/crawl', data=data).content.decode('utf-8')
    except:
        html_text = None
    return {'html_text': html_text}


if __name__ == '__main__':
    liebiaoye_qingqiu.consume()
    neirongye_qingqiu.consume()
    crawl_qingqiu.consume()
