# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  reactor subsystem
  -----------------

  Event-based, Hivy orchestrator

  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''

import sh
from hivy.logger import logger
import hivy.utils as utils

log = logger(__name__)


class Serf(object):
    ''' Serf wrapper, see www.serfdom.io '''

    enable = False

    def __init__(self, path='/usr/local/bin/serf'):
        try:
            self.serf = sh.Command(path)
            self.enable = utils.is_running('serf')
        except sh.CommandNotFound:
            log.warn('serf command not found', path=path)
            self.serf = None

        if self.enable:
            log.info('reactor enabled')
        else:
            log.warning('reactor disabled')

    def _serf_command(self, command, node_ip):
        ''' Safely perform the given serf subcommand '''
        if self.enable:
            try:
                feedback = self.serf(command, node_ip)
                flag = True
            except Exception, error:
                feedback = error.message
                flag = False
        else:
            feedback = 'serf is desactivated, abort'
            flag = False
        log.info('ran command', command=command, flag=flag, feedback=feedback)
        return str(feedback), flag

    def version(self):
        if self.enable:
            version = self.serf('--version').split('\n')[:-1]
        else:
            version = 'unknown'
        return version

    def register_node(self, node_ip):
        ''' Contact the serf agent of the given node to join the cluster'''
        log.info('registering node', ip=node_ip)
        return self._serf_command('join', node_ip)

    def unregister_node(self, node_ip):
        ''' Mark the given node agent as "left" '''
        #FIXME There is no effect, agent still as "failed"
        log.info('unregistering node', ip=node_ip)
        return self._serf_command('force-leave', node_ip)
