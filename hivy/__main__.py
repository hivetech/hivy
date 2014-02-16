#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''Hivy

Usage:
  hivy -h | --help
  hivy --version
  hivy [--bind=<ip>] [--port=<port>] [-d | --debug] [--log <level>]

Options:
  -h --help       Show this screen.
  --version       Show version.
  --debug         Activates Flask debug
  --bind=<ip>     Listens on the given ip [default: 127.0.0.1]
  --port=<port>   Listens on the given port [default: 5000]
  --log=<level>   Log output level [default: debug]
'''

import sys
from docopt import docopt
from hivy import __version__
from hivy.core import main


if __name__ == '__main__':
    args = docopt(__doc__, version='Hivy, Hive api {}'.format(__version__))
    sys.exit(main(args))
