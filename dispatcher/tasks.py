import json
from celery import shared_task, Task
from .dispatcher import Signal
from . import const


def set_task_name(name):
    const.TASK_NAME = name


def get_task_name():
    return const.TASK_NAME


def register_tasks(logger):
    retry_countdown = (0, 2, 4, 6, 8, 10, 20, 40, 60, 60*2, 60*5, 60*10, 60*30, 60*60)

    class MyTask(Task):
        def on_failure(self, exc, task_id, args, kwargs, einfo):
            if logger:
                logger.warn('Task {}[{}] args: {}, kwargs: {}'.format(self.name, task_id, json.dumps(args), json.dumps(kwargs)), exc_info=einfo)
                logger.error('Task {}[{}] args: {}, kwargs: {}'.format(self.name, task_id, json.dumps(args), json.dumps(kwargs)))

        def on_retry(self, exc, task_id, args, kwargs, einfo):
            if logger:
                logger.warn('Retry task[{}] {}[{}] args: {}, kwargs: {}'.format(self.request.retries, self.name, task_id, json.dumps(args), json.dumps(kwargs)), exc_info=einfo)

    @shared_task(base=MyTask, bind=True, name=const.TASK_NAME, acks_late=True, reject_on_worker_lost=True,
        ignore_result=True)
    def trigger_signal(self, signal_name, sender, **kwargs):
        try:
            signal = Signal.get_by_name(signal_name)
            signal.send(sender, **kwargs)
        except Exception as exc:
            countdown = retry_countdown[min(self.request.retries, len(retry_countdown) - 1)]
            raise self.retry(exc=exc, countdown=countdown, max_retries=20)
