# -*- coding: utf-8 -*-
"""Thread safe sqlite3 worker.
"""

import logging
import os
import sqlite3

from .base_worker import BaseWorker

class DataBase(BaseWorker):

    def on_start(self, path_db, createdb_queries, callback):
        self.logger = logging.getLogger(__name__)
        self.do_commit = False
        if not os.path.isfile(path_db):
            self.logger.warn("Database does NOT exist. Creating a NEW database.")
            self.db_con = sqlite3.connect(path_db)
            # Activate foreign key support
            # See: https://www.sqlite.org/foreignkeys.html
            self.put_element("pragma foreign_keys = ON;")
            for query in createdb_queries[:-1]:
                self.put_element(query)
            self.put_element(createdb_queries[-1], callback=callback)
        else:
            self.db_con = sqlite3.connect(path_db)
            callback(None, None)


    def put_element(self, query, query_params={}, callback=lambda r, e: None, force_commit=False):
        self.logger.debug("queued element")
        self.queue.put(tuple([query, query_params, callback, force_commit]))


    def on_element(self, query, query_params, callback, force_commit):
        result, error = None, None  # Values for callback
        try:
            self.logger.debug("working query:{} params:{}".format(query, query_params))
            result = self.db_con.execute(query, query_params)
            if force_commit:
                self._commit()
            else:
                self.do_commit = True
        except Exception as e:
            self.logger.debug("exception: {}".format(e))
            error = e
        # Callback!
        callback(result, error)


    def _commit(self):
        self.logger.debug("commit")
        self.db_con.commit()
        self.do_commit = False


    def on_timeout(self):
        """Commit on timeout
        """
        if self.do_commit:
            self._commit()


    def on_end(self):
        self.db_con.close()
