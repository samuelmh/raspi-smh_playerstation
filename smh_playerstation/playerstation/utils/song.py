# -*- coding: utf-8 -*-


import math
import shlex
import subprocess


BITRATES = {  # See: https://trac.ffmpeg.org/wiki/Encode/MP3
    245: "0",
    225: "1",
    190: "2",
    175: "3",
    165: "4",
    130: "5",
    115: "6",
    100: "7",
    85: "8",
    65: "9"
}


def analyze(song_path, song_abspath):
    retval = {
        'path': song_path,
        'source': song_path.split('/')[0],
        'extension': song_path.split('.')[-1],
        'length': get_media_length(song_abspath),   # in seconds
    }
    if retval['source'] == 'youtube':
        # Caution, name can have '.' and  id can have '-' positional solution
        retval['youtube_id'] = song_path.split('.')[-2][-11:]
    return retval


def get_media_length(song_abspath):
    try:
        result = subprocess.Popen(
            'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(shlex.quote(song_abspath)),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True
        )
        output = result.communicate()
        retval = int(math.ceil(float(output[0].strip())))
    except Exception:
        retval = -1
    return retval


def encode(song_abspath, file_out_abspath, bitrate=245, mono=False):
    retval = True
    try:
        subprocess.Popen(
            'ffmpeg -i {song_in} {quality} {mono} {song_out}'.format(
                song_in=shlex.quote(song_abspath),
                quality="-q:a {0}".format(BITRATES.get(bitrate, "0")),
                mono="-ac 1" if mono else "",
                song_out=shlex.quote(file_out_abspath),
            ),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True
        )
    except Exception:
        retval = False
    return retval
