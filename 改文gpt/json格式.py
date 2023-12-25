import pandas as pd


def count_characters(string):
    count = 0
    for char in string:
        if ord(char) < 128:  # 判断是否为ASCII字符
            count += 1
        else:
            count += 2
    return count


# 读取xlsx文件，跳过标头和列表序号
df = pd.read_excel('txt.xlsx', header=None, index_col=None)


lst = []
keyong_tishici = ''
num = 0
tishici = '请你作为一个资深的小说文案修改师，请绝对严格的方式遵循以下几点要求：1.如果哪些句子违反了你的内容协议，将此句子改成你内容协议可接受的范围同时尽量保留其原意。2.绝对保证有多少条原句子就有多少条改后句子不可以多也不可以少，例如有5条原句，改后句子也必须只有5条。3.将我发给你的小说片段句子进行修订，在保留原意的同时提高句子的复杂性。4.修订应侧重于词汇增强，例如，句子 "我此时正在悠闲地睡觉 "可修改为 "我此时正在沙发上悠闲地睡觉"。5.允许句子之间上下文关联。6.格式为严格标准化的 JSON 格式，例如 [{"1":"句子1"}，{"2":"句子2"}，{"3":"句子3"}......]。修订后的句子也必须以相同的 JSON 格式返回。请严格遵循上诉几点要求，下面我将发送给你小说句子：'
# 遍历第一列数据
for index, row in df.iterrows():
    first_column_text = row.iloc[0]
    lst.append({str(index): first_column_text})

    tishici_and_juzi = tishici + str(lst)
    zifu_num = count_characters(tishici_and_juzi)
    if zifu_num > 2500:
        with open(str(num)+'.txt', 'w', encoding='utf-8') as f:
            f.write(keyong_tishici)
        num += 1
        lst = [{str(index): first_column_text}]
        tishici_and_juzi = tishici + str(lst)
    else:
        keyong_tishici = tishici_and_juzi

with open(str(num)+'.txt', 'w', encoding='utf-8') as f:
    f.write(keyong_tishici)



