class HookABC(object):
    def on_task_retry(self, signal_name, sender):
        pass

    def on_task_trigger_signal(self, signal_name, sender):
        pass

    def on_task_execute_signal_receiver(self, signal_name, sender, target_receiver):
        pass

    def on_task_execute_signal_receiver_success(self, signal_name, sender, target_receiver):
        pass

    def on_task_execute_signal_receiver_error(self, signal_name, sender, target_receiver):
        pass
