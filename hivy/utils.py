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
import docker
import requests
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
    ''' `pgrep` returns an error code if no process was found '''
    try:
        pgrep = sh.Command('/usr/bin/pgrep')
        pgrep(process)
        flag = True
    except sh.ErrorReturnCode_1:
        flag = False
    return flag


def generate_random_name(size=8, chars=string.ascii_lowercase + string.digits):
    ''' Create a random name to assign to a node '''
    return ''.join(random.choice(chars) for _ in range(size))


def docker_check():
    docker_url = os.environ.get('DOCKER_URL', 'unix://var/run/docker.sock')
    dock = docker.Client(base_url=docker_url, timeout=5)
    try:
        docker_version = dock.version()
        status = True
    except requests.ConnectionError, error:
        docker_version = {'error': str(error)}
        status = False
    except requests.Timeout, error:
        docker_version = {'error': str(error)}
        status = False
    return docker_version, status


def generate_unique_id():
    event_id = uuid.uuid4().get_urn()
    return event_id.split(':')[-1]
