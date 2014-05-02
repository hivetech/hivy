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
import dna.utils

log = dna.logging.logger(__name__)


def version():
    ''' Inspect salt and its dependencies versions '''
    return {sub_salt: sub_version
            for sub_salt, sub_version in salt.version.versions_information()}


class Saltstack(object):
    ''' Hivy interface to Saltstack. It uses it to manipulate images '''

    library = ['debug']

    def __init__(self):
        # TODO Generic use with remote salt master
        # TODO Generic use with proper authentification
        # Salt master is on the same machine, and run as the same user
        self.api = salt.client.LocalClient()
        # If not found, salt will check at the default location
        self.config = salt.config.master_config(os.environ.get('SALT_CONFIG'))
        self.root_data = os.environ.get('SALT_DATA', '/srv')
        self.master_ip = dna.utils.self_ip()
        log.info('salt client ready', ip=self.master_ip)

    def check(self):
        ''' Test the connection with the master '''
        return self.api.cmd('*', 'test.ping') != {}

    def switch_context(self, user, servers_pattern):
        ''' Generate top.sls file including user config '''
        filename = '/'.join([self.root_data, 'pillar', 'top.sls'])
        if user not in self.library:
            self.library.append(user)
        utils.write_yaml_data(
            filename, {'base': {servers_pattern: self.library}})

    def store_data(self, user, data):
        ''' Write user configuration into its dedicated state file '''
        filename = '/'.join([self.root_data, 'pillar', '{}.sls'.format(user)])
        utils.write_yaml_data(filename, data)

    def _read_pillar(self, servers_pattern='*'):
        ''' Use salt magic to acquire current pillar data '''
        log.info('reading pillar', minions=servers_pattern)
        return self.call('pillar.items', servers_pattern)

    def call(self, function, servers_pattern='*', *args, **kwargs):
        ''' Wrap a salt call '''
        log.info('running salt state',
                 function=function, minions=servers_pattern, args=args)
        if isinstance(args, str):
            args = [args]
        return self.api.cmd(servers_pattern, function, args, kwarg=kwargs)
