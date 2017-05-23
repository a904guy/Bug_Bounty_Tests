import multiprocessing
import threading
import time


class Run_Async:
    running_callback: multiprocessing.Process or threading.Thread = None
    method = None
    limit = None
    sleep = 0.5

    def __init__(self, method: str, limit: int = 16, sleep: float = 0.5):
        """
        Run_Async is a helper to minimize the amount of code written to run async callables
        
        Parameters
        ----------
        method : str
            Either 'multiprocessing' or 'threading'
        limit :
            The limit of concurrent jobs allowed
        
        Returns
        -------
        self
            a Run_Async instance
        
        Raises
        ------
        AssertError
            when method isn't of the two allowed values
        Exception
            when method is None
        """
        if method == 'multiprocessing':
            self.method = method
        if method == 'threading':
            self.method = method
        self.sleep = sleep

        # Validation
        if self.method is None and self.method == type(str) and self.method not in ['threading', 'multiprocessing']:
            raise Exception('run_async(method=%s or %s)' % ('threading', 'multiprocessing'))
        assert type(limit) == int
        # if limit > 30:
        #     Log().warning('You are running at a very high limit, this is dangerous for the CPU')
        self.limit = limit

    def start(self, target: callable, args: tuple = (), **kwargs):
        if self.method == 'multiprocessing':
            while self.should_wait():
                time.sleep(self.sleep)
            self.running_callback = multiprocessing.Process(target=target, args=args, **kwargs)
            self.running_callback.start()
        if self.method == 'threading':
            while self.should_wait():
                time.sleep(self.sleep)
            self.running_callback = threading.Thread(target=target, args=args, **kwargs)
            self.running_callback.start()
        return self

    def wait_on_callback(self):
        while self.running_callback.is_alive():
            time.sleep(self.sleep)

    def should_wait(self):
        if self.method == 'multiprocessing':
            if len(multiprocessing.active_children()) >= self.limit:
                return True
        if self.method == 'threading':
            if threading.active_count() - 1 >= self.limit:
                return True
        return False

    def join_all(self):
        if self.method == 'multiprocessing':
            for p in multiprocessing.active_children():
                p.join(self.sleep)
        if self.method == 'threading':
            while threading.active_count() - 1 > 0:
                time.sleep(self.sleep)
