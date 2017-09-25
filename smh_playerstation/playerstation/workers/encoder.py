# -*- coding: utf-8 -*-
"""Convert songs to mp3 format.
"""

import logging
import os

from .base_worker import BaseWorker
from ..utils import song as song_utils


class Encoder(BaseWorker):

    def on_start(self, path_songs, path_songs_encoded):
        self.logger = logging.getLogger(__name__)
        self.PATH_SONGS = path_songs
        self.PATH_SONGS_ENCODED = path_songs_encoded


    def put_element(self, path_song, path_encoded, bitrate, mono):
        self.logger.debug("queued element")
        self.queue.put(tuple([path_song, path_encoded, bitrate, mono]))


    def on_element(self, path_song, path_encoded, bitrate, mono):
        abspath_song = os.path.join(self.PATH_SONGS, path_song)
        abspath_encoded = os.path.join(
            self.PATH_SONGS_ENCODED, path_encoded,
            os.path.splitext(os.path.basename(path_song))[0]  # Remove extension
        ) + '.mp3'
        path_encoded = os.path.dirname(abspath_encoded)
        if not os.path.exists(path_encoded):  # Create dirs
            os.makedirs(path_encoded)
        self.logger.debug("encode:{} into:{}".format(path_song, path_encoded))
        song_utils.encode(
            song_abspath=abspath_song,
            file_out_abspath=abspath_encoded,
            bitrate=bitrate,
            mono=mono
        )
