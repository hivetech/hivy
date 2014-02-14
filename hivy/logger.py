#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Hivy logger configuration
  -------------------------

  :copyright (c) 2014 Xavier Bruhier.
  :license: %LICENCE%, see LICENSE for more details.
'''

import sys
import calendar
import time
from structlog import wrap_logger
from structlog.processors import JSONRenderer
import logbook
import hivy.utils as utils


def add_unique_id(logger, method_name, event):
    event['id'] = utils.generate_unique_id()
    return event


def add_timestamp(logger, log_method, event_dict):
    event_dict['timestamp'] = calendar.timegm(time.gmtime())
    return event_dict


def setup(level='debug',
          show_log=False,
          filename='/tmp/hivy.log'):
    ''' Hivy formated logger '''

    # FIXME Same as in hivy.settings.py but can't use them : make reactor
    # importations fail
    log_format = (u'[{record.time:%m-%d %H:%M}] '
                  '{record.level_name}.{record.channel} {record.message}')

    level = level.upper()
    handlers = [
        logbook.NullHandler()
    ]
    if show_log:
        handlers.append(
            logbook.StreamHandler(sys.stdout,
                                  format_string=log_format,
                                  level=level))
    else:
        handlers.append(
            logbook.FileHandler(filename,
                                format_string=log_format,
                                level=level))

    return logbook.NestedSetup(handlers)


def logger(name=__name__):
    return wrap_logger(
        logbook.Logger(name),
        processors=[
            add_unique_id,
            add_timestamp,
            JSONRenderer(indent=2, sort_keys=True),
        ]
    )
