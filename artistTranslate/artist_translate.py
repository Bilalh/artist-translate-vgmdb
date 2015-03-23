# coding: utf-8
# Gets translations from vgmdb

"""
:copyright: 2014 Bilal Syed Hussain
:license: Apache 2.0
"""

import logging
import requests
import re
import jsonpickle

from multiprocessing import Pool
from pprint import pprint
from pathlib import Path
from mutagen.mp3 import EasyMP3 as MP3
from functools import partial

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(name)s:%(lineno)d:%(funcName)s: %(message)s', level=logging.WARN)

class Translation(object):
    def __init__(self, native):
        super(Translation, self).__init__()
        self.refs=[]
        self.english=""
        self.native=native

    def add_ref(self, ref):
        self.refs.append(ref)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
            ', '.join( key + "=" + self._format(key, getattr(self, key))
                for key in self.__dict__ if not key.startswith('_'))
                )

    def is_complete(self):
        if self.refs and self.english and self.native:
            return True
        else:
            return False


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

    return list(mapping.values())

def add_translation(t):
    english = search_for_artist(t.native)
    if english:
        t.english=english
    return t


def lookup_translations(artists):
    pool = Pool(processes=4)
    res = pool.map(add_translation, artists)
    return ([ artist for artist in res
        if artist.is_complete() and artist.english != artist.native ],
     [ artist for artist in res if not artist.is_complete() ])


def make_json(fp):
    artists = get_artists_from_mp3s(fp)
    with Path("artist_read.json").open('w') as f:
        f.write(jsonpickle.encode(artists) )

    with Path("artist_read.json").open('r') as f:
        mm = jsonpickle.decode(f.read())
        # pprint(mm)

    (translated, untranslated) = lookup_translations(artists)
    with Path("artist_translated.json").open('w') as f:
        f.write(jsonpickle.encode(translated) )

    with Path("artist_translated.json").open('r') as f:
        rr = jsonpickle.decode(f.read())
        pprint(rr)

    with Path("artist_untranslated.json").open('w') as f:
        f.write(jsonpickle.encode(untranslated) )

    with Path("artist_untranslated.json").open('r') as f:
        un = jsonpickle.decode(f.read())
        pprint(un)

    print("Stats:")
    print("Artists:      {}".format(len(mm)))
    print("Translated:   {}".format(len(rr)))
    print("Untranslated: {}".format(len(un)))
    print("Same:         {}".format(len(mm) - len(rr) - len(un)))

def tag_track_with_translation(english, fp):
    mp3 = MP3(str(fp))
    mp3['artist'] = [english]
    mp3.save()

def tag_tracks_with_translation(ts):
    for trans in ts:
        pa = partial(tag_track_with_translation, trans.english)

        pool = Pool(processes=4)
        pool.map(pa, trans.refs)

def tag_tracks_with_translation_json(json):
    with Path(json).open('r') as f:
        rr = jsonpickle.decode(f.read())
        pprint(rr)
        tag_tracks_with_translation(rr)
        print("Finished")


if __name__ == "__main__":
    # fp='/Users/bilalh/Music/iTunes/iTunes Music/Music/GUST'
    fp='/Users/bilalh/Desktop/ヘルミーナとクルス〜リリーのアトリエ もう一つの物語〜 オリジナルサウンドトラック'
    # make_json(fp)
    # tag_tracks_with_translation_json('artist_translated.json')

