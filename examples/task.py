import logging
from dispatcher import init_dispatcher
from celery import Celery


app = Celery('tasks', broker='redis://localhost')
app.conf.update(broker_transport_options={'visibility_timeout': 5})

logger = logging.getLogger('test')
init_dispatcher('.', '.', logger)
