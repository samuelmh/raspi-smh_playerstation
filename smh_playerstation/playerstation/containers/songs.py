
import logging
import os
import time

from ..utils import song as song_utils
from ..utils import sql


class Songs:

    def __init__(self, path_songs, worker_db, worker_encoder, worker_youtube_dl):
        self.logger = logging.getLogger(__name__)
        self.PATH_SONGS = path_songs
        self.w_db = worker_db
        self.w_encoder = worker_encoder
        self.w_youtube_dl = worker_youtube_dl
        self.songs_list = dict()  # Already added songs
        self.youtube_ids = set()  # Already downloaded YTB song IDs
        self.refresh_info()


    #
    ### Primitives
    #

    def add_song(self, path_song):
        """Add a song to the collection
        """
        self.logger.debug("add song {}".format(path_song))
        if path_song not in self.songs_list:
            song_abspath = os.path.join(self.PATH_SONGS, path_song)
            song = song_utils.analyze(path_song, song_abspath)
            # Song structure as it came from the DB
            song_db_like = {path_song: {k.upper():v for k,v in song.items() if k in ('path', 'length', 'extension', 'source')} }
            self.w_db.put_element(
                sql.SONGS_CREATE,
                song,
                lambda _,e: self.songs_list.update(song_db_like) if not e else None
            )
            if song['source'] == 'youtube':
                self.w_db.put_element(
                    sql.SONGS_YOUTUBE_CREATE,
                    song,
                    lambda _,e: self.youtube_ids.add(song['youtube_id']) if not e else None
                )
        else:
            self.logger.warning("Song {} already exists".format(path_song))


    def encode(self, path_song, path_encoded="", bitrate=130, mono=False):
        """Encode a song into an mp3 file
        """
        self.w_encoder.put_element(path_song, path_encoded, bitrate, mono)


    def download_from_youtube(self, youtube_id, path=''):
        """Download a song from youtube and add it to the collection.
        """
        if youtube_id not in self.youtube_ids:
            self.youtube_ids.add(youtube_id)
            self.w_youtube_dl.put_element(
                youtube_id, path,
                lambda path_song,e: self.add_song(path_song) if e==None else None
            )
        else:
            self.logger.warning("Youtube ID {} already downloaded".format(youtube_id))


    def refresh_info(self, sync=False):
        """Refresh list of downloaded & youtube songs.
        If sync, blocking operation.
        """
        self.logger.debug("refresh")
        def refresh_songs(songs, e):
            # Songs dictionary in memory
            self.logger.debug("refreshing song IDs")
            if e:
                self.logger.warning("{e}".format(e))
            else:
                songs.row_factory = lambda cursor, row: {
                    col[0]: row[idx]
                    for idx, col in enumerate(cursor.description)
                }
                self.songs_list = {x['PATH']: x for x in songs}
            nonlocal flag_songs
            flag_songs = True
        def refresh_ytb_ids(ytb_ids, e):
            # Youtube IDs in memory
            self.logger.debug("refreshing youtube IDs")
            if e:
                self.logger.warning("{e}".format(e))
            else:
                self.youtube_ids = {x[0] for x in ytb_ids}
            nonlocal flag_ytb_ids
            flag_ytb_ids = True
        flag_songs, flag_ytb_ids = False, False  # True when performed query
        self.w_db.put_element(
            sql.SONGS_READ,
            callback=refresh_songs
        )
        self.w_db.put_element(
            sql.SONGS_YOUTUBE_READ_IDS,
            callback=refresh_ytb_ids
        )
        while sync and not (flag_songs and flag_ytb_ids):  # Block
            self.logger.debug("waiting for refreshing...")
            time.sleep(1)


    #
    ### Extended functionalities
    #
    def scan_new_songs(self, refresh=True):
        """Look for new songs and add them to the collection.
        """
        self.logger.debug("scan new songs")
        if refresh:
            self.refresh_info(sync=True)  # blocking call
        for dirpath, _, filenames in os.walk(self.PATH_SONGS):
            for name in filenames:
                song_abspath = os.path.join(dirpath, name)  # Absolute path
                path_song = song_abspath[len(self.PATH_SONGS) + 1:]  # Relative path
                self.add_song(path_song)


    def rescan_collection(self):
        """Delete all songs from DB and scan all songs.
        """
        self.logger.debug("rescan collection")
        self.songs_list, self.youtube_ids = dict(), set()
        self.w_db.put_element(  # Foreign keys will delete from YOUTUBE_SONGS
            sql.SONGS_DELETE,
            callback=lambda result,e: self.scan_new_songs(refresh=False)
        )
