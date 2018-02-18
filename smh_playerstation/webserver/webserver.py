# -*- coding: utf-8 -*-
"""Player Station Microservice
"""


import logging.config

from flask import Flask
from flask_cors import CORS

from ..playerstation.playerstation import PlayerStation
from ..import config

from . views.api.v1_0 import V1_0
from . views.client import Client  # client


def init_playerstation():
    return PlayerStation(
        path_db=config.PATH_DB,
        path_songs=config.PATH_SONGS,
        path_songs_youtube=config.PATH_SONGS_YOUTUBE,
        path_songs_encoded=config.PATH_SONGS_ENCODED,
        player_command=config.PLAYER_COMMAND
    )


def get_app(ps):
    app = Flask(
        config.APP_NAME,
        static_folder=config.PATH_CLIENT+'/static'  # client
    )
    app.config.from_object(config)
    CORS(app)
    try:
        app.config.from_envvar(config.APP_NAME)
    except:
        pass
    ps.start()
    # Initialize views
    V1_0(
        app=app,
        url_prefix='/api/v1.0',
        playerstation=ps
    )
    Client(  # client
        app=app,
        url_prefix='/',
        path_client=config.PATH_CLIENT
    )
    return(app)



if __name__ == '__main__':
    logging.config.fileConfig(config.LOGGING_CONF_FILE)
    server = get_app(init_playerstation())
    server.run(host=config.HOST, port=config.PORT)
