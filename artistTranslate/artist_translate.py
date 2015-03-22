# coding: utf-8
"""
:copyright: 2014 Bilal Syed Hussain
:license: Apache 2.0
"""
from bs4 import BeautifulSoup
from multiprocessing import Pool
from pprint import pprint

import logging
import os
import requests
import shutil
import re

from pathlib import Path
from mutagen.mp3 import EasyMP3 as MP3
from collections import defaultdict
import json
import jsonpickle

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(name)s:%(lineno)d:%(funcName)s: %(message)s', level=logging.WARN)

class Translation(object):
    def __init__(self, native):
        super(Translation, self).__init__()
        self.refs=[]
        self.english=None
        self.native=native

    def add_ref(self, ref):
        self.refs.append(ref)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
            ', '.join( key + "=" + self._format(key, getattr(self, key))
                for key in self.__dict__ if not key.startswith('_'))
                )

    def _format(self, key, value):
        if key == "refs":
            if len(value) == 0:
                raise
            return "[len={}]".format(len(value))
        else:
            return str(value)




def search_for_artist(name):
    search_url='http://vgmdb.net/search?do=results_artist'
    r =requests.post(search_url, data=dict(artist=name))
    m=re.search(r"<a href='/artist/\d+'>(.*) \({}\)".format(name), r.text)
    if m and m.groups():
        return m.groups()[0].strip()
    else:
        return None


def get_artist_name(fp):
    mp3 = MP3(str(fp))
    if 'artist' in mp3:
        if mp3['artist']:
            return (mp3['artist'][0], fp)

    return (None, fp)


def get_artists_from_mp3s(base_dir):
    base = Path(base_dir)
    mp3s_names = list(base.glob('**/*.mp3'))

    pool = Pool(processes=4)
    mapping = {}

    for (k, v) in pool.map(get_artist_name, mp3s_names):
        if not k:
            continue
        if k not in mapping:
            t = Translation(k)
            mapping[k] = t
            mapping[k].add_ref(v)

    return mapping

if __name__ == "__main__":
    fp='/Users/bilalh/Music/iTunes/iTunes Music/Music/GUST'
    mapping = get_artists_from_mp3s(fp)
    with Path("artist_read.json").open('w') as f:
        f.write(jsonpickle.encode(mapping) )

    with Path("artist_read.json").open('r') as f:
        mm = jsonpickle.decode(f.read())
        pprint(mm)


