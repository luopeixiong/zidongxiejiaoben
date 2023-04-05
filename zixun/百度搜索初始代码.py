import requests  # 发送请求
from bs4 import BeautifulSoup  # 解析页面
import pandas as pd  # 存入csv数据
import os  # 判断文件存在
from time import sleep  # 等待间隔
import random  # 随机
import re  # 用正则表达式提取url
from requests.utils import get_encodings_from_content
import chardet
from urllib.parse import quote

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "www.baidu.com",
    # 需要更换Cookie
    "Cookie": 'BIDUPSID=BD4D9668AE78ED4E71CCC15E5A39386B; PSTM=1649385737; BAIDUID=BD4D9668AE78ED4E375CAD33698C1EBA:FG=1; BDUSS=k4dWs5UWlGRm9QZHFjaENwNHV5RnR-eVNsZTY4bmlLTH5yTG1ycDMtR2hDcTFqSVFBQUFBJCQAAAAAAAAAAAEAAACMHwA50ru49tPQ1r7H4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKF9hWOhfYVjZH; BDUSS_BFESS=k4dWs5UWlGRm9QZHFjaENwNHV5RnR-eVNsZTY4bmlLTH5yTG1ycDMtR2hDcTFqSVFBQUFBJCQAAAAAAAAAAAEAAACMHwA50ru49tPQ1r7H4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKF9hWOhfYVjZH; BD_UPN=12314753; ispeed_lsm=0; BAIDUID_BFESS=BD4D9668AE78ED4E375CAD33698C1EBA:FG=1; ZFY=vhBBbv6afYFOl49LSCpH2yIydp0tg2zNU0BCDxAZHSw:C; BA_HECTOR=0424aga1240k01ala5010kfn1hujamb1l; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; baikeVisitId=1d262693-040a-4cac-af5f-8026f4f7fd53; __bid_n=184f647c9e7f5b32c44207; FPTOKEN=xlnzbVwTVNt0K4b3w6YaD4rZjbZXgmKUJBDE7YWbWGNQ5Q6HMC5PEWSInIHwT60JK9d4/XPdfpdIqsfrOrNRAYLdITBOqNkNw02QegfuWXsoD2P1tNjHFQY6acCB+6FwLwcwgFhsqCi4RU7LItItTsV5VZuQ3Z8dHOO5KKqaJB0USuxq9dQzatbyQr11uBBENCaAl/S0uWIBGiBox4F6RUfxJJlvKghfCMtF8UCINnp4d+qRIeltSmA0G4tJsfUvYVXnJyk8UR5qCfa+GxkmOiHGq+mjEHT9clTvp3rR9fpW07x5CCEHKFgPFveMkQU7rsFuKrouv7H2dMNjCxsgin0cBgiWCjVOaSzq5UdNsks0fERJmP0f6gq/eQP+JRob6epwE96fkaHWk1ffNtsIXA==|mwW3zQn+c5TBs0RlB4wdTfyaZZigAI5OOFvAyh+3zKE=|10|3732bd9d84f137c7ac2ba46063d700b4; RT="z=1&dm=baidu.com&si=7e438407-c306-4d3e-9fce-c658fe25a25b&ss=le2krefy&sl=6&tt=34y&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=22rz&nu=13jr2gp3p&cl=1shb&ul=bw6x&hd=bwam"; BD_HOME=1; H_PS_PSSID=38188_36548_38094_38128_37910_38151_37990_38176_38171_37797_36802_37926_38088_37900_26350_38139_38008_37881; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=6; H_PS_645EC=a870hwJ08dG5WIKoYCsJYaWVSmH1y4N8HehmZRByirjsbujAZepN4AXl%2B3CJgToweeIE; BDSVRTM=221'
}


def baidu_search(v_keyword, v_result_file, v_max_page):
	"""
	爬取百度搜素结果
	:param v_keyword: 爬取前几页
	:param v_result_file: 搜索关键词
	:param v_max_page: 保存文件名
	:return: None
	"""
	# 获得每页搜索结果
	for page in range(v_max_page):
		print('开始爬取第{}页'.format(page + 1))
		wait_seconds = random.uniform(1, 2)  # 等待时长秒
		print('开始等待{}秒'.format(wait_seconds))
		# sleep(wait_seconds)  # 随机等待
		keywords = quote(v_keyword)
		url = 'https://www.baidu.com/s?wd={}&pn={}'.format(v_keyword, str(page * 10))
		html = requests.get(url, headers=headers).text
		soup = BeautifulSoup(html, 'html.parser')
		result_list = soup.find_all(class_='result c-container new-pmd ')
		print('正在爬取:{},共查询到{}个结果'.format(url, len(result_list)))
		kw_list = []  # 关键字
		page_list = []  # 页码
		title_list = []  # 标题
		href_list = []  # 百度的链接
		real_url_list = []  # 百度的链接
		desc_list = []  # 简介
		site_list = []  # 网站名称
		for result in result_list:
			title = result.find('a').text
			print('title is: ', title)
			href = result.find('a')['href']
			real_url = get_real_url(v_url=href)
			try:
				desc = result.find(class_='c-abstract').text
			except:
				desc = ""
			try:
				site = result.finf(class_='c-showucl c-color-gray ').text
			except:
				site = ""
			kw_list.append(v_keyword)
			page_list.append(page + 1)
			title_list.append(title)
			href_list.append(href)
			real_url_list.append(real_url)
			desc_list.append(desc)
			site_list.append(site)
			df = pd.DataFrame(
				{
					'关键词': kw_list,
					'页码': page_list,
					'标题': title_list,
					'百度链接': href_list,
					'真实链接': real_url_list,
					'简介': desc_list,
					'网站名称': site_list,
				}
			)
			if os.path.exists(v_result_file):
				header = None
			else:
				header = ['关键词', '页码', '标题', '百度链接', '真实链接', '简介', '网站名称']  # csv文件标头
			df.to_csv(v_result_file, mode='a+', index=False, header=header, encoding='utf_8_sig')
			print('结果保存成功:{}'.format(v_result_file))


def get_real_url(v_url):
	"""
	获取百度链接真实地址
	:param v_url: 百度链接地址
	:return: 真实地址
	"""
	r = requests.get(v_url, headers=headers, allow_redirects=False)  # 不允许重定向
	if r.status_code == 302:  # 如果返回302，就从响应头获取真实地址
		real_url = r.headers.get('Location')
	else:  # 否则从返回内容中用正则表达式提取出来真实地址
		real_url = re.findall("URL='(.*?)'", r.text)[0]
	print('real_url is:', real_url)
	return real_url


if __name__ == '__main__':
	search_keyword = '巴楚县人民政府'  # 搜索的关键词
	max_page = 5
	result_file = '爬取百度_{}_前{}页.csv'.format(search_keyword, max_page)  # 保存结果的文件名
	# # 如果结果文件存在，先删除
	# if os.path.exists(result_file):
	# 	os.remove(result_file)
	# 	print('结果文件({})存在,已删除'.format(result_file))
	# 	# 开始吧取
	baidu_search(v_keyword=search_keyword, v_result_file=result_file, v_max_page=max_page)
