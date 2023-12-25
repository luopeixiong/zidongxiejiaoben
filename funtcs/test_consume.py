import time
from funboost import boost, BrokerEnum


@boost('test_rpc_queue', is_using_rpc_mode=True, broker_kind=BrokerEnum.REDIS_ACK_ABLE, concurrent_num=200)
def add(a, b):
    time.sleep(3)
    return a + b


if __name__ == '__main__':
    add.consume()
    