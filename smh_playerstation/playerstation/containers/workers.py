# -*- coding: utf-8 -*-
"""Container to store and manage workers.
"""

class Workers:

    def __init__(self):
        self.workers = dict()


    def add(self, name, worker):
        self.workers[name] = worker


    def start_all(self):
        for w in self.workers.values():
            if not w.isAlive():
                w.start()


    def stop_all_and_wait(self):
        for w in self.workers.values():
            w.stop()
        for w in self.workers.values():
            w.join()


    def get(self, name):
        return self.workers.get(name, None)


    def status(self):
        return {
            k: {
                'alive': v.isAlive(),
                'queue_size': v.queue.qsize()
            }
            for k, v in self.workers.items()
        }
