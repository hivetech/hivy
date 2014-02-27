# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''

import sh
import os
import string
import yaml
import random
import uuid
import docker
import requests
import dna.utils
from hivy import __version__


def api_url(resource):
    ''' Harmonize api endpoints '''
    return '/v{}/{}'.format(dna.utils.Version(__version__).major, resource)


def api_doc(resource, method='GET', **kwargs):
    ''' Wrap api endpoints with more details '''
    doc = '{} {}'.format(method, api_url(resource))
    params = '&'.join(['{}={}'.format(k, v) for k, v in kwargs.iteritems()])
    if params:
        doc = '?'.join([doc, params])
    return doc


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
    ''' Check if docker is properly accessible '''
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
    ''' Hivy GUID method '''
    event_id = uuid.uuid4().get_urn()
    return event_id.split(':')[-1]


def write_yaml_data(filepath, data):
    ''' Dump a dictionnary into a file as yaml '''
    with open(filepath, 'w') as yaml_fd:
        yaml_fd.write(yaml.dump(data))


def clean_request_data(request_data):
    data = {}
    genes = map(lambda x: x.encode('utf-8'), request_data.pop('gene'))

    for key, value in request_data.iteritems():
        data[key.encode('utf-8')] = \
            map(lambda x: x.encode('utf-8'), value) \
            if isinstance(value, list) else value.encode('utf-8')
    return genes, data
