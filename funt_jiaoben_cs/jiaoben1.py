from lxml import etree
from funboost import AioAsyncResult
import asyncio
from xiaofei_jiaoben import liebiaoye_qingqiu, neirongye_qingqiu, crawl_qingqiu
import re
import requests
from nb_log import get_logger

from items import *


logger1 = get_logger('logger1',)


class Spider:
    mun = 0
    shi = Shi()

    def __init__(self):
        self.name = '2321中国人民大学采购与招标管理中心'
        self.items_cource = '中国人民大学采购与招标管理中心'  # 不要加前面数字

        self.start_urls = [
        'http://cgzx.ruc.edu.cn/cggg/hwlcggg/index.htm'
        'http://cgzx.ruc.edu.cn/cggg/fwlcggg/index.htm',
        'http://cgzx.ruc.edu.cn/cggg/gccggg/index.htm',

        'http://cgzx.ruc.edu.cn/jggg/hwlcgjg/index.htm',
        'http://cgzx.ruc.edu.cn/jggg/fwlcgjg/index.htm',
        'http://cgzx.ruc.edu.cn/jggg/gccgjg/index.htm'
    ]
        self.allowed_domains = ['cgzx.ruc.edu.cn']

    async def test_get_result(self, liebiaoye_url):
        items = {}
        async_result = liebiaoye_qingqiu.push(liebiaoye_url, items)
        aio_async_result = AioAsyncResult(task_id=async_result.task_id)  # 这里要使用asyncio语法的类，更方便的配合asyncio异步编程生态
        big_items = await aio_async_result.result  # 注意这里有个await，如果不await就是打印一个协程对象，不会得到结果。这是asyncio的基本语法，需要用户精通asyncio。
        html_text = big_items['html_text']
        jiexi = etree.HTML(html_text)
        titlell = jiexi.xpath('//ul[contains(@class, "lists-ul")]/li/a/text()')
        urlhtml = jiexi.xpath('//ul[contains(@class, "lists-ul")]/li/a/@href')
        # nian_list = jiexi.xpath('/text()')
        # yue_list = jiexi.xpath('/text()')
        # ri_list = jiexi.xpath('/text()')
        # publishtime = ['-'.join(x) for x in zip(nian_list, yue_list, ri_list)]
        # publishtime = re.findall(r'\d{4}-\d{1,2}-\d{1,2}|\d{4}/\d{1,2}/\d{1,2}|\d{4}\.\d{1,2}\.\d{1,2}|\d{4}年\d{1,2}月\d{1,2}', etree.tostring(jiexi.xpath('//ul[contains(@class, "wp_article_list")]/li/div[2]')[0], encoding='utf-8').decode('utf-8'))
        print(len(titlell), len(urlhtml))
        for x in range(0, len(urlhtml)):
            title_panduan = re.findall('采购|招标|中选|成交|废标|流标|磋商|比选|中标', titlell[x])
            if not title_panduan:
                continue
            # items['publishtime'] = publishtime[x].replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            # zuihou_time = items['publishtime']
            items['source'] = self.items_cource
            items['notes'] = 'bscrapy'
            items['title'] = titlell[x].replace('...', '').replace('\n', '').replace('\t', '')
            url = str(urlhtml[x]).replace('&amp;', '&')
            url = url_pingjie(liebiaoye_url, url)
            items['original_url'] = url

            shifouchadao = self.shi.shishi(items['source'], str(url))

            if url and shifouchadao:
                items = self.zhaozhong_biao(liebiaoye_url, items)
                # 爬取内容页
                await self.html(liebiaoye_url, items)

    def zhaozhong_biao(self, liebiaoye_url, items):
        for x in ['jggg']:
            if x in liebiaoye_url:
                items['channel_id'] = 15  # 中标15  招标16
                break
            else:
                items['channel_id'] = 16  # 中标15  招标16
        return items

    async def html(self, url, items):
        async_result = neirongye_qingqiu.push(url, items)
        aio_async_result = AioAsyncResult(task_id=async_result.task_id)
        big_items = await aio_async_result.result
        html_text = big_items['html_text']
        jiexi = etree.HTML(html_text)
        items['content'] = etree.tostring(jiexi.xpath('//div[contains(@class, "main")]')[0], encoding='utf-8').decode('utf-8')
        publishtime = re.findall(r'\d{4}-\d{1,2}-\d{1,2}|\d{4}/\d{1,2}/\d{1,2}|\d{4}\.\d{1,2}\.\d{1,2}|\d{4}年\d{1,2}月\d{1,2}', etree.tostring(jiexi.xpath('//span[contains(@class, "date")]')[0], encoding='utf-8').decode('utf-8'))[0]
        items['publishtime'] = publishtime.replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-')
        await self.guding_xieru(url, items)

    async def guding_xieru(self, response_url, items):
        if items['title'] is not None and items['content'] is not None:
            if '>' in items['title']:
                items['title'] = re.sub(r'(<(.+?)>)', '', items['title']).strip()
            items['content'] = re.sub(r'((href|src)=["|\'])(/(?![/])((?![:]).)+?)(["|\'])',
                                      r'\g<1>' + response_url.split('/')[0] + '//' + response_url.split('/')[
                                          2] + r'\g<3>\g<5>',
                                      re.sub(r'((href|src)=["|\'])((?![/])((?![:]).)+?)(["|\'])',
                                             r'\g<1>' + response_url.replace(response_url.split("/")[-1],
                                                                             "") + r'\g<3>\g<5>',
                                             items['content']))  # 全自动补全升级版
            print(items['channel_id'], len(items['content']), items['publishtime'], items['title'], items['original_url'])  # 输出
            self.shi.shishi1(items['source'], str(response_url))
            form_data = zidianformdata(items)
            # html_text = requests.post('http://192.168.0.228/index.php/api/article/crawl', data=data)
            # print(html_text)
            # html_text3 = big_items3['html_text']
            async_result = crawl_qingqiu.push({'source': items['source'], 'url': response_url, **form_data})
            aio_async_result = AioAsyncResult(task_id=async_result.task_id)
            big_items = await aio_async_result.result
            if big_items['html_text']:
                self.shi.shishi1(items['source'], response_url)
                self.mun += 1
                logger1.info("------------------------------\n" + big_items['html_text'])
            else:
                logger1.warning("------------------------------\n{}".format(response_url))
        else:
            if items['content'] is None and items['title'] is None:
                logger1.warning('########################################content|title获取不完整： ', response_url)
            elif items['title'] is None:
                logger1.warning('########################################title获取不完整： ', response_url)
            elif items['content'] is None:
                logger1.warning('########################################content获取不完整： ', response_url)


if __name__ == '__main__':
    spider = Spider()
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(spider.test_get_result(liebiaoye_url)) for liebiaoye_url in spider.start_urls]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.stop()
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
