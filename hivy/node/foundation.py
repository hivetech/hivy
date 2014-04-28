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

import docker
from hivy.genetics.saltstack import Saltstack
from hivy.node.factory import NodeFactory
import dna.logging
import dna.utils

log = dna.logging.logger(__name__)


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
        name = name or dna.utils.generate_random_name()
        NodeFactory.__init__(self, image, name, role)

        self.state = Saltstack()

        # TODO Use self.consul.status['leader']
        self.environment.update({
            'SALT_MASTER': self.state.master_ip,
            'CONSUL_MASTER': self.state.master_ip
        })

    def forget(self):
        # TODO Gracefully shutdown consul node agent
        # self.consul.local_agent.force_leave(self.name)
        return 'not implemented', False

    def synthetize(self, profile, gene, data={}):
        ''' Apply the given saltstack state on the current image '''
        self.state.switch_context(profile, self.name)
        self.state.store_data(profile, data)
        cmd = 'state.sls' if gene in self.state.library else 'cmd.run'
        return self.state.call([cmd], self.name, args=[[gene]])

    # NOTE Consul should provide a more efficient way to do that
    def discover(self, link_name):
        '''
        Search for the given service and update its environment with
        connection informations
        '''
        try:
            link_node = self.dock.inspect_container(link_name)
        except docker.APIError, error:
            log.error('failed to discover link', error=error)
            return

        link_name = link_name.upper()
        tmp_env = {
            '{}_HOST'.format(link_name):
            link_node['NetworkSettings']['IPAddress'],
            '{}_PORTS_EXPOSED'.format(link_name):
            ','.join(map(lambda x: x.split('/')[0],
                         link_node['NetworkSettings']['Ports'].keys()))
        }
        for port_spec in link_node['NetworkSettings']['Ports']:
            port = port_spec.split('/')[0]
            tmp_env.update({
                '{}_PORT_{}'.format(link_name, port): port
            })
        self.environment.update(tmp_env)
        self.links.append(tmp_env)
