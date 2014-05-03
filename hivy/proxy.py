# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  :copyright (c) 2014 Xavier Bruhiere.
  :license: Apache 2.0, see LICENSE for more details.
'''

import os
from redis import Redis
import dna.logging

log = dna.logging.logger(__name__)


# TODO Check redis commands, assert are for current debug
class Hipache(object):
    '''
    Dynamic handler for hipache
    https://github.com/dotcloud/hipache
    '''

    def __init__(self, redis_host=None, redis_port=None):
        ''' Initialize hipache redis connection '''
        # Read third partie services from the env
        redis_host = redis_host or os.environ.get('REDIS_HOST', '0.0.0.0')
        redis_port = redis_port or os.environ.get('REDIS_PORT', 6379)

        # Prepare redis connection
        log.info('connecting to mapping manager (redis)')
        self.conn = Redis(host=redis_host, port=int(redis_port))

        # Initial empty configuration
        self._vhosts = {}

    @property
    def connected(self):
        return self.conn.ping()

    @property
    def mapping(self):
        return self._vhosts

    # TODO Add exception handlers
    def _register(self, frontend, value):
        # Update our vhosts little state machine
        if frontend not in self._vhosts:
            self._vhosts[frontend] = [value]
        else:
            self._vhosts[frontend].append(value)

        # Hipache compliant frontend key
        frontend = 'frontend:{}'.format(frontend)
        # Push to redis and return True on success
        return self.conn.rpush(frontend, value) >= 1

    def _get_backends(self, frontend):
        frontend = 'frontend:{}'.format(frontend)
        return self.conn.lrange(frontend, 0, -1)

    def remove_frontend(self, frontend):
        backends = self._vhosts.pop(frontend)
        log.info('removing frontend {} associated with {}'
                 .format(frontend, backends))
        frontend = 'frontend:{}'.format(frontend)
        return self.conn.delete(frontend) == 1

    # TODO reset=True => re-initialize
    def check_and_register_frontend(self, frontend, name, replace=False):
        if self._get_backends(frontend):
            if replace:
                assert self.remove_frontend(frontend)
                assert self._register(frontend, name)
            else:
                log.info('{} already set, doing nothing'.format(frontend))
        else:
            assert self._register(frontend, name)

    def map_backends(self, frontend, backends):
        # Most of the time we just want to map one new backend
        backends = backends if isinstance(backends, list) else [backends]
        for backend in backends:
            log.info('mapping {} to {}'.format(frontend, backend))
            assert self._register(frontend, backend)

    def reset(self):
        ''' Flush redis db '''
        log.info('reset mapping')
        self._vhosts = {}
        return self.conn.flushall()
