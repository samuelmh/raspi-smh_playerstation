# -*- coding: utf-8 -*-

# Root path for the project data: songs, db, etc
from .config_local import PATH_DATA, PATH_PROJECT, PATH_CONFIG


#
### Logging
#
LOGGING_CONF_FILE = PATH_CONFIG + '/logging.conf'


#
### Paths
#

# --__ Don't change __--

# Database
PATH_DB = PATH_DATA + '/db.sqlite'

# Songs
PATH_SONGS = PATH_DATA + '/songs'
PATH_SONGS_ENCODED = PATH_DATA + '/encoded'
PATH_SONGS_YOUTUBE = PATH_SONGS + '/youtube'

# Client
PATH_CLIENT = PATH_PROJECT+'/client'


#
### Music player
#
PLAYER = 'ffplay'

# Command to be executed by the player
PLAYER_COMMAND = {
    'ffplay': 'ffplay -loglevel quiet -nodisp -autoexit {file}',
    'pifm': 'ffmpeg -i {{file}}  -f s16le -ar 22.05k -ac 1 -filter "volume=2" - | sudo "{}" - 103.3'.format(PATH_PROJECT+'/extra/piFM/pifm')
}[PLAYER]


#
### Web server (Flask) config params
#
APP_NAME = 'SMH_PLAYERSTATION'
DEBUG = False
HOST = '0.0.0.0'
PORT = 8000
