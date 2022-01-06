import json
import traceback
from itertools import chain
from celery import shared_task, Task
from .dispatcher import Signal
from . import const
from celery.execute import send_task  # pylint: disable=import-error,no-name-in-module


def set_task_name(name):
    const.TASK_NAME = name


def get_task_name():
    return const.TASK_NAME


def set_receiver_task_name(name):
    const.RECEIVER_TASK_NAME = name


def get_receiver_task_name():
    return const.RECEIVER_TASK_NAME


def register_tasks(logger, hook):
    retry_countdown = (0, 2, 4, 6, 8, 10, 20, 40, 60, 60*2, 60*5, 60*10, 60*30, 60*60)

    class MyTask(Task):
        def on_failure(self, exc, task_id, args, kwargs, einfo):
            if logger:
                logger.error('Task {}[{}] args: {}, kwargs: {}'.format(self.name, task_id, json.dumps(args), json.dumps(kwargs)))

    def retry(self, signal_name, sender, kwargs, exceptions, finished_receivers=None):
        tb = ''.join(chain(*[traceback.format_exception(exc.__class__, exc, exc.__traceback__) for exc in exceptions]))
        logger.warn('Retry task {}[{}: {} from {}] finished_receivers: {}, kwargs: {}\n{}'.format(
            self.request.retries, self.name, signal_name, sender, finished_receivers, json.dumps(kwargs), tb))
        countdown = retry_countdown[min(self.request.retries, len(retry_countdown) - 1)]
        new_kwargs = self.request.kwargs
        if finished_receivers:
            new_kwargs['finished_receivers'] = finished_receivers
        self.retry(kwargs=new_kwargs, exc=exceptions[0], countdown=countdown, max_retries=20)
        if hook is not None:
            hook.on_task_retry(signal_name, sender)

    @shared_task(base=MyTask, bind=True, name=const.RECEIVER_TASK_NAME, acks_late=True, reject_on_worder_lost=True, ignore_result=True)
    def execute_signal_receiver(self, signal_name, sender, target_receiver=None, **kwargs):  # noqa
        if not target_receiver:
            return
        signal = Signal.get_by_name(signal_name)
        resp = signal.send_to_target_receiver(sender, target_receiver, **kwargs)
        if not resp:
            return
        res_receiver_key, r = resp
        if isinstance(r, Exception):
            retry(self, signal_name, sender, kwargs, [r])

        if hook is not None:
            hook.on_task_execute_signal_receiver(signal_name, sender, target_receiver)
            if isinstance(r, Exception):
                hook.on_task_execute_signal_receiver_error(signal_name, sender, target_receiver)
            else:
                hook.on_task_execute_signal_receiver_success(signal_name, sender, target_receiver)

    @shared_task(base=MyTask, bind=True, name=const.TASK_NAME, acks_late=True, reject_on_worker_lost=True,
        ignore_result=True)
    def trigger_signal(self, signal_name, sender, finished_receivers=None, **kwargs):
        signal: Signal = Signal.get_by_name(signal_name)
        finished_receivers = finished_receivers or []
        new_finished_receivers = []
        exceptions = []
        for receiver_key in signal.live_receiver_keys(sender):
            try:
                if receiver_key in finished_receivers:
                    continue
                named = {
                    "target_receiver": receiver_key
                }
                named.update(kwargs)
                send_task(const.RECEIVER_TASK_NAME, args=(signal_name, sender), kwargs=named)
                new_finished_receivers.append(receiver_key)
            except Exception as e:
                exceptions.append(e)
        if exceptions:
            new_finished_receivers.extend(finished_receivers or [])
            retry(self, signal_name, sender, kwargs, exceptions, finished_receivers=new_finished_receivers)

        if hook is not None:
            hook.on_task_trigger_signal(signal_name, sender)
