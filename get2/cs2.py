import time

time_stamp = 1672052781000
print(str(time_stamp)[:-3])

# 时间戳 => 结构化时间 => 时间字符串
time_str = time.strftime('%Y-%m-%d', time.localtime(int(str(time_stamp)[:-3])))
print(time_str)
# publishtime = time.strftime('%Y-%m-%d', time.localtime(int(str(x["docRelTime"])[:-3])))