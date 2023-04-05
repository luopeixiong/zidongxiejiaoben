import re

a = """<div class="zjy_top"><h1>标题</h1><p><span>信息来源：</span><span>更新时间：2023-03-13</span></p></div>"""
a_str_lst = list(a)
biaoqian_lst = [(match.group(), match.start(), match.end()) for match in re.finditer('<(((?![ |>]).)+)', a)]
print(a)
kaitou_biaoqian = []
num = 0
# TODO 目前可以处理当存在多的开头标签（也就是没有/的标签：<span>）的情况，当出现多的闭合标签会出现报错，因为我认为只会可能出现多的开头标签而不会出现多的闭合标签因为多的闭合标签会html出错
# TODO 请解决多个开头标签bug
while True:
    if len(biaoqian_lst) == num:
        break
    elif '/' not in biaoqian_lst[num][0]:
        kaitou_biaoqian.append(biaoqian_lst[num])
        num += 1
    else:
        if kaitou_biaoqian[-1][0] == biaoqian_lst[num][0].replace('/', ''):  # 如果当前闭合标签与开头标签列表的最后一个标签的名称一致（例：<div == <div.replace('/', '')，就删掉开头标签列表的最后一个标签
            kaitou_biaoqian.pop()
            num += 1
        else:
            del a_str_lst[kaitou_biaoqian[-1][1]:kaitou_biaoqian[-1][2]+1]
            kaitou_biaoqian.pop()

print(''.join(a_str_lst))