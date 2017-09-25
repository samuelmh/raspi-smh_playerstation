# -*- coding: utf-8 -*-

import logging
import os

import youtube_dl  # https://github.com/rg3/youtube-dl/blob/master/README.md

from .base_worker import BaseWorker


class YoutubeDL(BaseWorker):

    def on_start(self, path_songs, path_songs_youtube):
        self.logger = logging.getLogger(__name__)
        self.PATH_SONGS = path_songs
        self.PATH_SONGS_YOUTUBE = path_songs_youtube


    def put_element(self, youtube_id, path_dest, callback=lambda path,e: None):
        self.logger.debug("queued element")
        self.queue.put(tuple([youtube_id, path_dest, callback]))


    def on_element(self, youtube_id, path_dest, callback):
        self._callback = callback  # Store for later use in hook
        download_path = os.path.join(self.PATH_SONGS_YOUTUBE, path_dest)
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        ydl_opts = {
            'format': 'bestaudio/best',
            'progress_hooks': [self._on_finished],
            'outtmpl': os.path.join(
                download_path,
                '%(title)s-%(id)s.%(ext)s'
            )
        }
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        try:
            ydl.download([
                'http://www.youtube.com/watch?v={}'.format(youtube_id)
            ])
        except Exception as e:
            self.logger.debug("exception: {}".format(e))
            callback(None, e)


    def _on_finished(self, ydl_file):
        if ydl_file['status'] == 'finished':
            song_path = ydl_file['filename'][len(self.PATH_SONGS) + 1:]
            self._callback(song_path, None)
