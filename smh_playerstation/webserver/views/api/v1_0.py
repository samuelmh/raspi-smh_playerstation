# -*- coding: utf-8 -*-

import json

from flask import jsonify, request, send_from_directory, make_response

from .. import status


class V1_0(object):

    def __init__(self, app, url_prefix, playerstation):
        self.app = app
        self.url_prefix = url_prefix
        self.ps = playerstation
        self.ROUTES = {
            # Basic
            '/description': {
                'view_func': self.description_get,
                'methods': ['GET']
            },
            '/status': {
                'view_func': self.status_get,
                'methods': ['GET'],
            },
            '/shutdown': {
                'view_func': self.shutdown_get,
                'methods': ['GET'],
            },
            # Songs
            '/songs': {
                'view_func': self.songs_get,
                'methods': ['GET'],
            },
            '/songs/scan': {
                'view_func': self.songs_scan_get,
                'methods': ['GET'],
            },
            '/songs/rescan': {
                'view_func': self.songs_rescan_get,
                'methods': ['GET'],
            },
            '/songs/youtube': {
                'view_func': self.songs_youtube_get,
                'methods': ['GET'],
            },
            '/songs/youtube/download': {
                'view_func': self.songs_youtube_download_post,
                'methods': ['POST'],
            },
            # Player
            '/player': {
                'view_func': self.player_get,
                'methods': ['GET'],
            },
            '/player/playlist': {
                'view_func': self.player_playlist,
                'methods': ['POST', 'PUT'],
            },
            '/player/mode/<mode>': {
                'view_func': self.player_mode_post,
                'methods': ['POST'],
            },
            '/player/action/<action>': {
                'view_func': self.player_action_get,
                'methods': ['POST'],
            },
            # Playlists
            '/playlists': {
                'view_func': self.playlists_get,
                'methods': ['GET'],
            },
            '/playlists/<playlist_id>': {
                'view_func': self.playlists_modify,
                'methods': ['POST', 'DELETE'],
            },
        }
        for k, v in self.ROUTES.items():
            app.add_url_rule(
                rule=self.url_prefix + k,
                endpoint='api_v1_0_' + v['view_func'].__name__,
                **v
            )

    #
    # # Basic
    #
    def description_get(self):
        """Show API usage."""
        retval = {
            'service': 'smh_playerstation',
            'URL prefix': self.url_prefix,
            'description': 'REST API to control the smh_playerstation',
            'methods': {
                k: {
                    'methods': v['methods'],
                    'description': v['view_func'].__doc__,
                }
                for k, v in self.ROUTES.items()
            }
        }
        return(jsonify(retval), status.OK)

    def status_get(self):
        """Information  of the different components of the smh_playerstation."""
        ps_status = {
            'player': self.ps.player.status(),
            'workers': self.ps.workers.status()
        }
        return(jsonify(ps_status), status.OK)

    def shutdown_get(self):
        """Shutdown (safely) the server."""
        self.ps.stop()
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    #
    # # Songs
    #
    def songs_get(self):
        """List all the available songs.
        """
        retval = self.ps.songs.songs_list
        return(jsonify(retval), status.OK)

    def songs_scan_get(self):
        """Find new songs in the collection (fast).
        """
        self.ps.songs.scan_new_songs()
        retval = 'OK'
        return(jsonify(retval), status.OK)

    def songs_rescan_get(self):
        """Re-index the whole collection (slow).
        """
        self.ps.songs.rescan_collection()
        retval = 'OK'
        return(jsonify(retval), status.OK)

    def songs_youtube_get(self):
        """List all the Youtube song ids.
        """
        retval = list(self.ps.songs.youtube_ids)
        return(jsonify(retval), status.OK)

    def songs_youtube_download_post(self):
        """Download songs from Youtube and add it to the collection.
        """
        # POST params
        youtube_ids = request.json.get('youtube_ids')
        path = request.json.get('path', '')
        if not youtube_ids:
            return(
                jsonify({'error': 'youtube_id param required.'}),
                status.BAD_REQUEST
            )
        for youtube_id in youtube_ids.split():
            self.ps.songs.download_from_youtube(
                youtube_id=youtube_id,
                path=path
            )
        return(jsonify('OK'), status.OK)

    #
    # # Player
    #
    def player_get(self):
        """Show the status of the player: playlist, position, mode, etc.
        """
        retval = self.ps.player.status()
        return(jsonify(retval), status.OK)

    def player_playlist(self):
        """Extend or replace the player playlist.
        """
        song_ids = request.json.get('song_ids', False)
        if not song_ids:
            return(
                jsonify({'error': 'song_ids param required.'}),
                status.BAD_REQUEST
            )
        if request.method == 'POST':
            self.ps.player.add_list(files=song_ids)
        elif request.method == 'PUT':
            self.ps.player.set_list(files=song_ids)
        return(jsonify('OK'), status.OK)

    def player_action_get(self, action):
        """Control the player.
        """
        print(action)
        retval = (jsonify('OK'), status.OK)
        if action == "play":
            self.ps.player.play()
        elif action == "play_next":
            self.ps.player.play_next()
        elif action == "stop":
            self.ps.player.stop()
        else:
            retval = (
                {'error': 'action MUST be: play, play_next or stop'},
                status.BAD_REQUEST
            )
        return(retval)

    def player_mode_post(self, mode):
        """Set the player mode.
        """
        if mode in self.ps.player.MODES:
            retval = (jsonify('OK'), status.OK)
            self.ps.player.set_mode(mode)
        else:
            retval = (jsonify({'error': 'mode not found'}), status.BAD_REQUEST)
        return retval

    #
    # # Playlists
    #

    def playlists_get(self):
        """
        """
        return(jsonify(self.ps.playlists.playlists_list), status.OK)


    def playlists_modify(self, playlist_id):
        """
        POST params:
            songs: json list of song ids
        """
        if request.method == 'DELETE':
            self.ps.playlists.delete(playlist_id)
        elif request.method == 'POST':
            # POST params
            playlist_songs = request.json.get('songs', False)
            if playlist_songs==False:
                return(
                    jsonify({'error': 'songs param required.'}),
                    status.BAD_REQUEST
                )
            self.ps.playlists.upsert(playlist_id, playlist_songs)
        return(jsonify('OK'), status.OK)
