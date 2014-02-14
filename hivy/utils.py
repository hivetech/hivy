# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''

import sh
import os
import string
import random
import uuid
from hivy import __version__


class Version(object):
    ''' Provide a convenient way to manipulate version '''
    def __init__(self):
        _version = __version__.split('.')
        self.major = int(_version[0])
        self.minor = int(_version[1])
        self.patch = int(_version[2])


def api_url(resource):
    ''' Harmonize api endpoints '''
    return '/v{}/{}'.format(Version().major, resource)


def is_running(process):
    try:
        pgrep = sh.Command('/usr/bin/pgrep')
        pgrep(process)
        flag = True
    except sh.ErrorReturnCode_1:
        flag = False
    return flag


def is_available(command):
    ''' Mark "command" as available if running and allowed '''
    return (is_running(command) and
            os.environ.get('USE_{}'.format(command.upper())))


def generate_random_name(size=8, chars=string.ascii_lowercase + string.digits):
    ''' Create a random name to assign to a node '''
    return ''.join(random.choice(chars) for _ in range(size))


def generate_unique_id():
    event_id = uuid.uuid4().get_urn()
    return event_id.split(':')[-1]
