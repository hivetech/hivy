# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  test helpers
  ------------

  Provide some useful functions for efficient tests

  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''

import os
import dna.utils


def docker_required(function):
    ''' Run the provided function only if we can reach the docker server '''
    def inner(*args, **kwargs):
        ''' decorator '''
        _, status = dna.utils.docker_check()
        if status and is_allowed('docker'):
            return function(*args, **kwargs)
        else:
            pass
    return inner


def serf_required(function):
    ''' Run the provided function only if we can reach the serf cluster '''
    def inner(*args, **kwargs):
        ''' decorator '''
        if dna.utils.is_running('serf') and is_allowed('serf'):
            return function(*args, **kwargs)
        else:
            pass
    return inner


def salt_required(function):
    ''' Run the provided function only if we can reach the salt master '''
    def inner(*args, **kwargs):
        ''' decorator '''
        if dna.utils.is_running('salt-master') and is_allowed('salt'):
            return function(*args, **kwargs)
        else:
            pass
    return inner


def consul_required(function):
    ''' Run the provided function only if we can reach the salt master '''
    def inner(*args, **kwargs):
        ''' decorator '''
        if dna.utils.is_running('consul') and is_allowed('consul'):
            return function(*args, **kwargs)
        else:
            pass
    return inner


def is_allowed(command):
    ''' Mark "command" as available if running and allowed '''
    return os.environ.get('USE_{}'.format(command.upper()))
