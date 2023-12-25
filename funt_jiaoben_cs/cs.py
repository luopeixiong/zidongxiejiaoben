import asyncio

from funboost import AioAsyncResult
from cs_xiaofei import add
import random
import datetime


async def test_get_result(i):
    async_result = add.push(i, i * 2)
    aio_async_result = AioAsyncResult(task_id=async_result.task_id)  # 这里要使用asyncio语法的类，更方便的配合asyncio异步编程生态
    print(await aio_async_result.result)  # 注意这里有个await，如果不await就是打印一个协程对象，不会得到结果。这是asyncio的基本语法，需要用户精通asyncio。
    # 获取当前时间
    current_time = datetime.datetime.now().time()
    print("当前时间:", current_time)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(test_get_result(j)) for j in range(5)]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.stop()
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
    print('结束')
