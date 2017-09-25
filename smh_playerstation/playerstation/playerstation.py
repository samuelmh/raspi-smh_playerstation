

from . import workers
from . import containers
from . utils import sql


class PlayerStation:

    def __init__(self, path_db, path_songs, path_songs_youtube, path_songs_encoded, player_command):
        # Config constants
        self.path_db = path_db
        self.path_songs = path_songs
        self.path_songs_youtube = path_songs_youtube
        self.path_songs_encoded = path_songs_encoded
        self.player_command = player_command
        # Containers
        self.workers = None
        self.songs = None
        self.playlists = None
        self.player = None


    def _start_after_db(self, result, exception):
        """First, initialize the DB things, then this.
        """
        self.workers.start_all()
        self.player = containers.Player(self.path_songs)
        self.player.set_command(self.player_command)
        self.songs = containers.Songs(
            path_songs=self.path_songs,
            worker_db=self.workers.get('db'),
            worker_encoder=self.workers.get('encoder'),
            worker_youtube_dl=self.workers.get('youtube_dl')
        )
        self.playlists = containers.Playlists(
            worker_db=self.workers.get('db')
        )


    def start(self):
        """Launch all the containers
        """
        self.workers = containers.Workers()
        # Add workers
        self.workers.add('db', workers.DataBase(
            path_db=self.path_db,
            createdb_queries=sql.DB_CREATE,
            callback= self._start_after_db
        ))
        self.workers.add('encoder', workers.Encoder(
            path_songs=self.path_songs,
            path_songs_encoded=self.path_songs_encoded
        ))
        self.workers.add('youtube_dl', workers.YoutubeDL(
            path_songs=self.path_songs,
            path_songs_youtube=self.path_songs_youtube
        ))
        # Start -> DB worker callback start all workers
        self.workers.get('db').start()


    def stop(self):
        self.player.stop()
        self.workers.stop_all_and_wait()
