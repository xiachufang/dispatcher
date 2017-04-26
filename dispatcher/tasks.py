import json
import traceback
from itertools import chain
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
                logger.error('Task {}[{}] args: {}, kwargs: {}'.format(self.name, task_id, json.dumps(args), json.dumps(kwargs)))

    def retry(self, signal_name, sender, finished_receivers, kwargs, exceptions):
        tb = ''.join(chain(*[traceback.format_exception(exc.__class__, exc, exc.__traceback__) for exc in exceptions]))
        logger.warn('Retry task {}[{}: {} from {}] finished_receivers: {}, kwargs: {}\n{}'.format(
            self.request.retries, self.name, signal_name, sender, finished_receivers, json.dumps(kwargs), tb))
        countdown = retry_countdown[min(self.request.retries, len(retry_countdown) - 1)]
        new_kwargs = self.request.kwargs
        new_kwargs['finished_receivers'] = finished_receivers
        self.retry(kwargs=new_kwargs, exc=exceptions[0], countdown=countdown, max_retries=20)

    @shared_task(base=MyTask, bind=True, name=const.TASK_NAME, acks_late=True, reject_on_worker_lost=True,
        ignore_result=True)
    def trigger_signal(self, signal_name, sender, finished_receivers=None, **kwargs):
        signal = Signal.get_by_name(signal_name)
        resp = signal.send_robust(sender, finished_receivers=finished_receivers, **kwargs)
        new_finished_receivers = [lookup_key for lookup_key, r in resp if not isinstance(r, Exception)]
        exceptions = [r for lookup_key, r in resp if isinstance(r, Exception)]
        if exceptions:
            new_finished_receivers.extend(finished_receivers or [])
            retry(self, signal_name, sender, new_finished_receivers, kwargs, exceptions)
