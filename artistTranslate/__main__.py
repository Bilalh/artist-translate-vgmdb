#!/usr/bin/env python
# coding: utf-8
"""
:copyright: 2014 Bilal Syed Hussain
:license: Apache 2.0
"""

import logging


def main():
	rootLogger = logging.getLogger()
	consoleHandler = logging.StreamHandler()
	consoleHandler.setLevel(logging.WARN)
	consoleHandler.setFormatter(logging.Formatter('[Log]    %(message)s'))
	logging.getLogger().addHandler(consoleHandler)



if __name__ == '__main__':
	main()

