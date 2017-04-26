from celery import Celery
from signals import ORDER_CREATED

app = Celery('tasks', broker='redis://localhost')

ORDER_CREATED.send_async(None, order_id=1, user_id=1, shop_id=1)
