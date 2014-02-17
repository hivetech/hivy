#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Hivy Flask app
  --------------

  Entry point, invoke as `http` or `python -m httpie`

  :copyright (c) 2014 Hive Tech, SAS.
  :license: %LICENCE%, see LICENSE for more details.
'''

from hivy.core import main
import sys


if __name__ == '__main__':
    sys.exit(main())
