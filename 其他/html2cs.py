import lxml
from lxml import etree
from lxml.html.clean import Cleaner



cleaner = Cleaner()
cleaner.javascript = True
cleaner.page_structure = False
cleaner.style = True


with open('index2.html', 'r', encoding='utf-8') as f:
    html_str = f.read()

x = lxml.html.fromstring(html_str)
etree_root = cleaner.clean_html(x)
dom_tree = etree.ElementTree(etree_root)

jiexi = etree.HTML('index2.html')

for e in dom_tree.iter():
    xpath = dom_tree.getpath(e)
    print(xpath)
    print(jiexi.xpath(xpath))
    print('-----------')
    # print(xpath)

