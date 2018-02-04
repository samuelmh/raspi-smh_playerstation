# -*- coding: utf-8 -*-


import logging
import os
import random
import shlex
import subprocess
import signal
import threading
import time


class CommandPlayer(threading.Thread):

    def __init__(self, command, callback):
        """Constructor

        Parameters
        ----------
        command : str
            Command to execute.
        callback: function
            Function to call after the command is successfully executed.
        """
        self.command = command
        self.callback = callback
        self.process = None
        super(self.__class__, self).__init__()


    def run(self):
        """Thread method override.
        """
        # From: https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
        self.process = subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE, 
            shell=True,
            preexec_fn=os.setsid
        )
        self.process.wait()
        if self.process.returncode == 0:  # Process was not killed
            self.callback()

    def stop(self):
        """Stop the command execution.
        """
        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)


class Player(object):

    # PLAY MODES
    MODES = {
        'LIST': 0,  # Play list once
        'REPEAT_LIST': 1,  # Repeat list
        'REPEAT_FILE': 2,  # Repeat file
        'RANDOM': 3,  # Play a random file
    }
    MODES_INV = {v: k for k, v in MODES.items()}  # For status


    def __init__(self, path_songs):
        self.logger = logging.getLogger(__name__)
        self.path_songs = path_songs
        self.is_playing = False
        self.tstamp_play = None  # When command was launched
        self.playlist = []  # File list
        self.playlist_id = -1  # Which file to play
        self.mode = self.MODES['LIST']
        self.player_command = None  # Command used to play an element
        self.thread = None  # Thread that runs the command

    #
    # # Player settings
    #

    def set_command(self, command):
        """Set which command use to play a file.

        Parameters
        ----------
        command : str
            This string will be formatted.
            Fields: {field}

        Returns
        -------
        None
        """
        self.player_command = command
        return None


    def set_mode(self, mode):
        """Set the play mode.

        Parameters
        ----------
        mode : int
            Player.MODES element.
        """
        if mode in self.MODES:
            self.mode = self.MODES[mode]


    #
    # # Playlist
    #

    def set_list(self, files):
        self.playlist = files
        self.playlist_id = 0 if files else -1


    def add_list(self, files):
        """Add some elements to be played.

        Parameters
        ----------
        files : [str]
            Elements to be appended to the current playlist.
        """
        if files:
            if not list:
                self.set_list(files)
            else:
                self.playlist.extend(files)

    #
    # # Internal functions
    #

    def _callback(self):
        """Callback function to invoke for the next element.
        """
        self.is_playing = False
        self.play_next()

    #
    # # Player control
    #

    def play_next(self):
        """Play the next element in the playlist.
        """
        self.stop()
        play_flag = True
        if self.playlist:
            if self.mode == self.MODES['LIST']:
                if self.playlist_id < len(self.playlist)-1:
                    self.playlist_id += 1
                else:
                    play_flag = False
            elif self.mode == self.MODES['REPEAT_LIST']:
                self.playlist_id = (self.playlist_id + 1) % len(self.playlist)
            elif self.mode == self.MODES['RANDOM']:
                self.playlist_id = random.randint(0, len(self.playlist) - 1)
        if play_flag:
            self.play()


    def play(self, position=None):
        """Play the current element in the playlist.
        """
        if position!=None and (0 <= position < len(self.playlist)):
            self.playlist_id = position
            self.stop()
        if not self.is_playing:
            self.logger.debug("play: {}".format(os.path.join(self.path_songs, self.playlist[self.playlist_id])))
            self.tstamp_play = time.time()
            self.is_playing = True
            self.thread = CommandPlayer(
                command=self.player_command.format(
                    file=os.path.join(self.path_songs, self.playlist[self.playlist_id])
                ),
                callback=self._callback
            )
            self.thread.start()


    def stop(self):
        """If an element is being played, stop.
        """
        if self.is_playing:
            self.is_playing = False
            self.tstamp_play = None
            self.thread.stop()


    def status(self):
        """Player status
        """
        retval = {
            'mode': self.MODES_INV[self.mode],
            'playlist': self.playlist,
            'position': self.playlist_id,
            'playing_time': -1
        }
        if self.is_playing:
            retval['playing_time'] = int(time.time() - self.tstamp_play)
        return retval
