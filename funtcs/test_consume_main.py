from test_consume import add

def show_result(status_and_result: dict):
    print(status_and_result)


for i in range(100):
    async_result = add.push(i, i * 2)
    # print(async_result.result)   # 执行 .result是获取函数的运行结果，会阻塞当前发布消息的线程直到函数运行完成。
    async_result.set_callback(show_result)  # 使用回调函数在线程池中并发的运行函数结果

