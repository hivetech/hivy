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


log = logger('hivy.reactor.' + __name__)


class Serf(object):
    ''' Serf wrapper, see www.serfdom.io '''

    def __init__(self, path='/usr/local/bin/serf'):
        try:
            self.serf = sh.Command(path)
        except sh.CommandNotFound:
            log.warn('serf command not found', path=path)
            self.serf = None

    def _serf_command(self, command, node_ip):
        ''' Safely perform the given serf subcommand '''
        if utils.is_available('serf'):
            try:
                feedback = self.serf(command, node_ip)
                flag = True
            except Exception, error:
                feedback = error.message
                flag = False
        else:
            feedback = 'serf is desactivated, abort'
            flag = False
        return str(feedback), flag

    def version(self):
        return self.serf('--version').split('\n')[:-1]

    def register_node(self, node_ip):
        ''' Contact the serf agent of the given node to join the cluster'''
        return self._serf_command('join', node_ip)

    def unregister_node(self, node_ip):
        ''' Mark the given node agent as "left" '''
        #FIXME There is no effect, agent still as "failed"
        return self._serf_command('force-leave', node_ip)
