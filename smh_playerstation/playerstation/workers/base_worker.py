# -*- coding: utf-8 -*-

import queue
import threading


class BaseWorker(threading.Thread):

    TIMEOUT = 3  # Seconds to wait for an item in the queue

    def __init__(self, alt_queue=None, **kwargs):
        """kwargs will be passed as params to on_start function.
        """
        self.queue = alt_queue if alt_queue else queue.Queue()
        self.working = False
        self.start_params = kwargs
        super().__init__()


    def stop(self):
        """Stop the worker
        """
        self.working = False


    def run(self):
        """Worker is running
        """
        self.on_start(**self.start_params)
        self.working = True
        while self.working:
            try:
                element = self.queue.get(timeout=self.TIMEOUT)
                self.on_element(*element)
            except queue.Empty:
                self.on_timeout()
            except Exception as e:
                self.logger.warning("Exception: {}".format(e))
        self.on_end()


    #
    # Override as needed
    #

    def on_start(self, **start_params):
        """Use this function as your constructor.
        """
        pass


    def on_element(self, element):
        """Executed for each element.
        """
        pass


    def put_element(self, element):
        """Redefine this method if you change the on_element() input params.
        """
        self.queue.put(tuple(element))


    def on_timeout(self):
        """Executed when there are no elements.
        """
        pass


    def on_end(self):
        """Excuted when terminating the worker.
        """
        pass
