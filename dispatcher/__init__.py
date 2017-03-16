
"""Multi-consumer multi-producer dispatching mechanism
Originally based on pydispatch (BSD) http://pypi.python.org/pypi/PyDispatcher/2.0.1
See license.txt for original license.
Heavily modified for Django's purposes.
"""

from .dispatcher import Signal, receiver  # NOQA
from .tasks import register_tasks, set_task_name   # NOQA
from .discover import discover_receivers  # NOQA


def init_dispatcher(path, base_path, logger=None, task_name=None):
    if task_name:
        set_task_name(task_name)
    register_tasks(logger)
    discover_receivers(path, base_path)
