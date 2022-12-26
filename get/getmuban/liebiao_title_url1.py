titlell_xpath = '{title_xpath}'
    titlell_xpath_re = r"title=[\'|\"](.+?)[\'|\"]"
    urlhtml_xpath = '{url_xpath}'~titlell = response.xpath(self.titlell_xpath).re(self.titlell_xpath_re)