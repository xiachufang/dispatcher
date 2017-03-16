from dispatcher import receiver
from signals import ORDER_CREATED


@receiver(ORDER_CREATED)
def order_created(sender, order_id, user_id, shop_id, **kwargs):
    raise Exception('error')
    # print 'sleep 4'
    # import time
    # time.sleep(10)
    print 'receive order order_created'
