    def parse(self, response, *args, **kwargs):
        if response.status == 200 and len(response.text) > 1:
            titlell = response.xpath('{title_xpath}').extract()
            # titlell = response.xpath('{title_xpath}').re(r"title=[\'|\"](.+?)[\'|\"]")
            urlhtml = response.xpath('{url_xpath}').re(r"href=[\'|\"](.+?)[\'|\"]")
            nian_list = response.xpath('{nianyue_xpath}').re(r"\d【4】-\d【1,2】|\d【4】/\d【1,2】|\d【4】\.\d【1,2】|\d【4】年\d【1,2】")
            yue_list = response.xpath('').extract()
            ri_list = response.xpath('{ri_xpath}').extract()
            publishtime = ['-'.join(x) for x in zip(nian_list, yue_list, ri_list)]
            publishtime = response.xpath('{time_xpath}').re(r"\d【4】-\d【1,2】-\d【1,2】|\d【4】/\d【1,2】/\d【1,2】|\d【4】\.\d【1,2】\.\d【1,2】|\d【4】年\d【1,2】月\d【1,2】")
            print(len(titlell), len(urlhtml), len(publishtime), response.url)
            if len(titlell) != len(urlhtml) or len(titlell) != len(publishtime) or len(urlhtml) != len(publishtime):
                self.logger.info("##########################shujubuyizhihuokong")
            for x in range(0, len(publishtime)):
                # title_panduan = re.findall('采购|招标|中选|成交|废标|流标|磋商|比选|中标|合同|分包|单一来源', titlell[x])
                # if not title_panduan:
                #     continue
                items = ShishicesiItem()
                items['publishtime'] = publishtime[x].replace('.', '-').replace(' ', '').replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '').replace('\n', '').replace('\t', '')
                self.zuihou_time = items['publishtime']
                items['source'] = self.items_cource
                items['notes'] = self.notes
                items['title'] = titlell[x].replace('...', '').replace('\n', '').replace('\t', '')
                # items['daili'] = 1
                url = str(urlhtml[x]).replace('&amp;', '&')
                url = self.url_pingjie(response, url)
                items['original_url'] = url.replace('&amp;', '&')
                shifouchadao = self.shi.shishi(items['source'], str(url))
                self.logger.info('%s@@@chadedao') if not shifouchadao else self.logger.info('%s@@@chabudao')
                if url and shifouchadao:
                    # 判断招中标
                    self.zhaozhong_biao(response, items)
                    # 爬取列表内各个url的数据
                    yield scrapy.Request(url=url, callback=self.html, meta=【'items': items】)
                    # yield scrapy.FormRequest(url=url.split('|')[0], method="POST", headers=self.headers, body=url.split('|')[1], callback=self.html, meta=【'items': items】)
                    # items['content'] = x['contentdetail']
                    # yield from self.guding_xieru2(response, items)
            # # 存在下一页翻页
            # yield from self.xiayiye_fanye(response)

