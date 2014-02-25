# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Hivy Saltstack tool
  -------------------

  Use saltstack client api to configure nodes
  http://docs.saltstack.com/ref/clients/index.html

  :copyright (c) 2014 Hive Tech, SAS.
  :license: %LICENCE%, see LICENSE for more details.
'''

import os
import salt.client
import salt.config
import hivy.utils as utils
import dna.logging

log = dna.logging.logger(__name__)


class Saltstack(object):

    library = ['debug']

    def __init__(self):
        # TODO Generic use with remote salt master
        # TODO Generic use with proper authentification
        # Salt master is on the same machine, and run as the same user
        self.api = salt.client.LocalClient()
        self.config = salt.config.master_config(os.environ.get('SALT_CONFIG'))
        self.root_data = os.environ.get('SALT_DATA', '/srv')
        log.info('salt client ready')

    def switch_context(self, user, servers_pattern):
        ''' Generate top.sls file including use config '''
        filename = '/'.join([self.root_data, 'pillar', 'top.sls'])
        self.library.append(user)
        utils.write_yaml_data(
            filename, {'base': {servers_pattern: self.library}})

    def store_data(self, user, data):
        filename = '/'.join([self.root_data, 'pillar', '{}.sls'.format(user)])
        utils.write_yaml_data(filename, data)

    def _master_ip(self):
        ''' It will be used by the created node to find its salt master '''
        #TODO Get local ip using dna
        return os.environ.get('SALT_MASTER_URL', 'localhost')

    def _read_pillar(self, servers_pattern='*'):
        log.info('reading pillar', minions=servers_pattern)
        return self._run('pillar.items', servers_pattern)

    def _run(self, function, servers_pattern='*', args=[], kwargs={}):
        log.info('running salt state',
                 function=function, minions=servers_pattern, args=args)
        if isinstance(args, str):
            args = [args]
        return self.api.cmd(servers_pattern, function, args, kwarg=kwargs)
