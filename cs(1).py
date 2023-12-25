import sys

def menu():
    print('''\n欢迎使用PYTHON学生通讯录
1：添加学生
2：删除学生
3：修改学生信息
4：搜索学生
5：显示全部学生信息
6：退出并保存''')


def xiugai(xinxi_lst):
    you = False
    for k, v in dic.items():
        if xinxi_lst[1] == k:
            you = True
            print('Success')
            dic[k][0] = xinxi_lst[2]
            dic[k][1] = xinxi_lst[3]
            break
    if not you:
        print('No Record')



dic = {'张自强': ['12652141777', '材料'], '庚同硕': ['14388240417', '自动化'], '王岩': ['11277291473', '文法']}


xinxi_lst = []

for x in range(4):
    try:
        inp = input()
    except:
        break
    xinxi_lst.append(inp)

if xinxi_lst[0] == '3':
    print(dic)
    menu()
    xiugai(xinxi_lst)
    print(dic)
else:
    pass
