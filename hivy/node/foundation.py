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

import time
import hivy.reactor.reactor as reactor
import hivy.utils as utils
from hivy.genetics.saltstack import Saltstack
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

    def __init__(self, image, name=None, role='node'):
        name = name or utils.generate_random_name()
        NodeFactory.__init__(self, image, name, role)

        self.serf = reactor.Serf()
        self.state = Saltstack()

        self.environment.update({
            'SALT_MASTER': self.state._master_ip(),
        })

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

    def synthetize(self, profile, gene, data={}):
        self.state.switch_context(profile, self.name)
        self.state.store_data(profile, data)
        cmd = 'state.sls' if gene in self.state.library else 'cmd.run'
        return self.state._run([cmd], self.name, args=[[gene]])
