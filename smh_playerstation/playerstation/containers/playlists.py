
import json
import logging
import time

from ..utils import sql


class Playlists:

    def __init__(self, worker_db):
        self.logger = logging.getLogger(__name__)
        self.w_db = worker_db
        self.playlists_list = dict()
        self.refresh_info()


    #
    ### Primitives
    #

    def refresh_info(self, sync=False):
        """Refresh playlists.
        If sync, blocking operation.
        """
        self.logger.debug("refresh")
        def refresh_playlists(playlists, e):
            # Playlists dictionary in memory
            self.logger.debug("refreshing playlists")
            if e:
                self.logger.warning("{e}".format(e))
            else:
                playlists.row_factory = lambda cursor, row: {
                    col[0]: row[idx]
                    for idx, col in enumerate(cursor.description)
                }
                self.playlists_list = {x['ID']: json.loads(x['SONGS']) for x in playlists}
            nonlocal flag_playlists
            flag_playlists = True
        flag_playlists = False  # True when performed query
        self.w_db.put_element(
            sql.PLAYLISTS_READ,
            callback=refresh_playlists
        )
        while sync and not flag_playlists:  # Block
            self.logger.debug("waiting for refreshing...")
            time.sleep(1)


    def upsert(self, list_id, songs_ids):
        """songs_ids: [str]
        """
        self.w_db.put_element(
            sql.PLAYLISTS_UPSERT,
            {"list_id": list_id, "songs_ids": json.dumps(songs_ids)},
            lambda _,e: self.playlists_list.update({list_id: songs_ids}) if not e else None
        )


    def delete(self, list_id):
        self.w_db.put_element(
            sql.PLAYLISTS_DELETE,
            {"list_id": list_id},
            lambda _,e: self.playlists_list.pop(list_id) if not e else None
        )
