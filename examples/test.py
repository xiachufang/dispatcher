from celery import Celery
from signals import ORDER_CREATED, SIGNAL_B, SIGNAL_A

app = Celery('tasks', broker='redis://localhost')

ORDER_CREATED.send_async(None, order_id=1, user_id=1, shop_id=1)


SIGNAL_A.send_sync(order_id=1, user_id=2)

SIGNAL_B.send_sync(order_id=1, user_id=2)