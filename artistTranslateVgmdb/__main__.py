#!/usr/bin/env python
# coding: utf-8
"""
:copyright: 2014 Bilal Syed Hussain
:license: Apache 2.0
"""

import logging
import argparse
import sys
from os.path import expanduser, exists
import os
from .artist_translate import make_json, tag_tracks_with_translation_json
from pathlib import Path

logger = logging.getLogger(__name__)


def main():
    rootLogger = logging.getLogger()
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.WARN)
    consoleHandler.setFormatter(logging.Formatter('[Log]    %(message)s'))
    logging.getLogger().addHandler(consoleHandler)

    handle_args()

def handle_args():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_json = subparsers.add_parser('json', help='Create the json mapping')

    parser_json.add_argument('base_dir', help='Music dir')
    parser_json.add_argument('json_dir', help='dir to put json')
    parser_json.set_defaults(func=cmd_json)

    parser_tag = subparsers.add_parser('tag', help='tag using a json mapping')
    parser_tag.add_argument('json', help='json to use')
    parser_tag.set_defaults(func=cmd_tag)

    args = parser.parse_args()
    if args.__dict__:
        args.func(args)
    else:
        parser.parse_args("-h")



def cmd_json(args):
    args.base_dir = expanduser(args.base_dir)
    if not exists(args.base_dir):
        print("%s does not exist" % args.base_dir )
        sys.exit(3)

    args.json_dir = expanduser(args.json_dir)
    os.makedirs(args.json_dir, exist_ok=True)

    # fp='/Users/bilalh/Desktop/ヘルミーナとクルス〜リリーのアトリエ もう一つの物語〜 オリジナルサウンドトラック'
    make_json(Path(args.base_dir), Path(args.json_dir))


def cmd_tag(args):
    args.json_dir = expanduser(args.json)
    if not exists(args.json):
        print("%s does not exist" % args.json )
        sys.exit(3)

    tag_tracks_with_translation_json(Path(args.json))



if __name__ == '__main__':
    main()

