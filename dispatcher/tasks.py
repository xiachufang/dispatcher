import json
from celery import shared_task, Task
from .dispatcher import Signal
from . import const


def set_task_name(name):
    const.TASK_NAME = name


def get_task_name():
    return const.TASK_NAME


def register_tasks(logger):

    class MyTask(Task):
        def on_failure(self, exc, task_id, args, kwargs, einfo):
            if logger:
                logger.error('Task {}[{}] args: {}, kwargs: {}'.format(self.name, task_id, json.dumps(args), json.dumps(kwargs)), exc_info=einfo)

    @shared_task(base=MyTask, bind=True, name=const.TASK_NAME, acks_late=True, reject_on_worker_lost=True,
        ignore_result=True, autoretry_for=(Exception,))
    def trigger_signal(self, signal_name, sender, **kwargs):
        signal = Signal.get_by_name(signal_name)
        signal.send(sender, **kwargs)
