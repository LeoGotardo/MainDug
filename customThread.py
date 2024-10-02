import threading
import ctypes

class CustomThread(threading.Thread):
    """
    Initialize CustomThread Object

    Args:
        group (object): Thread Group.
        target (callable): Target function to call when thread starts.
        name (str): Thread name.
        args (tuple): Arguments to pass to the target function.
        kwargs (dict): Keyword arguments to pass to the target function.
        daemon (bool): If True, the thread will be a daemon thread.
        verbose (bool): Verbosity level.

    Returns:
        The return value of the target function if it exists.
    """
    def _init_(self, group=None, target=None, name=None, args=(), kwargs={}, daemon=None, verbose=None):
        super(CustomThread, self)._init_(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._return = None
        self._stop_event = threading.Event()

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args, **kwargs):
        super(CustomThread, self).join(*args, **kwargs)
        return self._return

    def get_id(self):
        # Returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        else:
            for id, thread in threading._active.items():
                if thread is self:
                    return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')