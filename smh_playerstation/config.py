# -*- coding: utf-8 -*-

# Root path for the project data: songs, db, etc
from .config_local import PATH_DATA, PATH_PROJECT


#
### Logging
#
LOGGING_CONF_FILE = PATH_DATA + '/logging.conf'


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


#
### Music player
#
PLAYER = 'ffplay'

# Command to be executed by the player
PLAYER_COMMAND = {
    'ffplay': 'ffplay -loglevel quiet -nodisp -autoexit "{file}"',
    'pifm': 'avconv -i "{{file}}"  -f s16le -ar 22.05k -ac 1  -filter "volume=volume=3" - | sudo "{}" - 96.6'.format(PATH_PROJECT+'/extra/piFM/pifm')
}[PLAYER]


#
### Web server
#
APP_NAME = 'SMH_PLAYERSTATION'
DEBUG = False
HOST = '0.0.0.0'
PORT = 8000
