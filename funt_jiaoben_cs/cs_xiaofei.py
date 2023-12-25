import time
from funboost import boost, BrokerEnum
import random


@boost('test_rpc_queue', is_using_rpc_mode=True, broker_kind=BrokerEnum.REDIS)
def add(a, b):
    num = random.randint(1, 10)
    print('延迟：' + str(num))
    time.sleep(num)
    return a + b


if __name__ == '__main__':
    add.consume()
