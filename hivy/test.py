# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  test helpers
  ------------

  Provide some useful functions for efficient tests

  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''

import hivy.utils as utils


def docker_required(function):
    ''' Run the provided function only if we can reach the docker server '''
    def inner(*args, **kwargs):
        ''' decorator '''
        if utils.is_available('docker'):
            return function(*args, **kwargs)
        else:
            pass
    return inner


def serf_required(function):
    ''' Run the provided function only if we can reach the serf cluster '''
    def inner(*args, **kwargs):
        ''' decorator '''
        if utils.is_available('serf'):
            return function(*args, **kwargs)
        else:
            pass
    return inner