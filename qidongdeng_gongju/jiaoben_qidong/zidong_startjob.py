from datetime import datetime

# 获取当前时间
current_time = datetime.now()

# 获取当前小时
current_hour = datetime.now().hour

# 打印当前小时
print("当前小时:", current_hour)

# 判断当前时间是否在00:00到08:59之间
if 0 <= current_hour <= 8:
    print("当前时间在00:00到08:59之间")
else:
    print("当前时间不在00:00到08:59之间")
