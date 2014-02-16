#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  containers topology management
  ------------------------------

  Provide a high level interface for Hivy containers management

  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''

import os
import time
import hivy.reactor.reactor as reactor
import hivy.utils as utils
from hivy.node.factory import NodeFactory
from hivy.logger import logger

log = logger(__name__)


class NodeFoundation(NodeFactory):
    '''
    Basic container with additional methods to make it Hivy-ready :
      * Serf agent interface for service orchestration
      * Salt master interface for node system configuration

    salt-master must run as the same user as this script (usually system user)
    Change in /etc/salt/master:
      - user: username
      - root_dir: /home/username
    '''

    #local = salt.client.LocalClient()

    def __init__(self, image, name=None, role='node'):
        name = name or utils.generate_random_name()
        NodeFactory.__init__(self, image, name, role)

        self.environment.update({
            'SALT_MASTER': self._salt_master_ip(),
        })

        self.serf = reactor.Serf()

    #TODO Detection salt master ip
    def _salt_master_ip(self):
        ''' It will be used by the created node to find its salt master '''
        return os.environ.get('SALT_MASTER_URL', 'localhost')

    def _check(self, servers):
        ''' Check if servers are up '''
        #return self.local.cmd(servers, 'test.ping')
        return {'localhost': 'ok'}

    def register(self, retry=3):
        '''
        Contact the node to make it to join the serf cluster so we can track it
        '''
        infos = self.inspect()
        success = False
        while retry and not success:
            log.info('trying to register node',
                     retry=retry, ip=infos['node']['virtual_ip'])
            feedback, success = \
                self.serf.register_node(infos['node']['virtual_ip'])
            time.sleep(10)
            retry -= 1
        log.info('registered node',
                 retry=retry, ip=infos['node']['virtual_ip'],
                 success=success, feedback=feedback)
        return feedback, success

    def forget(self):
        ''' Tell the serf cluster the node has left '''
        infos = self.inspect()
        return self.serf.unregister_node(infos['node']['virtual_ip'])
