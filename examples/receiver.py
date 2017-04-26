from dispatcher import receiver
from signals import ORDER_CREATED


@receiver(ORDER_CREATED)
def order_created(sender, order_id, user_id, shop_id, **kwargs):
    print 'order_created'
    # print 'before raise'
    # raise ValueError('error')
    # print 'sleep 4'
    # import time
    # time.sleep(10)
    # print 'receive order order_created'


@receiver(ORDER_CREATED)
def order_created2(sender, order_id, user_id, shop_id, **kwargs):
    raise ValueError('error')
    # print 'sleep 4'
    # import time
    # time.sleep(10)


@receiver(ORDER_CREATED)
def order_created3(sender, order_id, user_id, shop_id, **kwargs):
    raise ValueError('error3')
    # print 'sleep 4'
    # import time
    # time.sleep(10)
