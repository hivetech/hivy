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
import dna.logging
import dna.utils
import pyconsul.http
import hivy.utils
from hivy.genetics.saltstack import Saltstack
import hivy.node.factory as factory

log = dna.logging.logger(__name__)


class NodeFoundation(factory.NodeFactory):
    '''
    Basic container with additional methods to make it Hivy-ready :
      * Serf agent interface for service orchestration
      * Salt master interface for node system configuration

    salt-master must run as the same user as this script (usually system user)
    Change in /etc/salt/master:
      - user: username
      - root_dir: /home/username
    '''

    def __init__(self, image, name=None, docker_url=None):
        name = name or dna.utils.generate_random_name()
        factory.NodeFactory.__init__(self, image, name, docker_url)

        self.state = Saltstack()
        self.consul = pyconsul.http.Consul()

        leader = self.consul.leader
        consul_master = leader.split(':')[0] if 'error' not in leader else ''

        self.environment.update({
            'SALT_MASTER': self.state.master_ip,
            'CONSUL_MASTER': consul_master,
            # TODO Use consul to read logstash address
            'LOGSTASH_SERVER': os.environ.get('LOGSTASH_SERVER', '0.0.0.0')
        })

    def forget(self):
        return self.consul.local_agent.force_leave(self.name)

    @hivy.utils.normalize_link_name
    def _build_link_env(self, link_name, link_network):
        link_env = {
            '{}_HOST'.format(link_name): link_network['IPAddress'],
            '{}_PORTS_EXPOSED'.format(link_name):
            ','.join(map(lambda x: x.split('/')[0],
                         link_network['Ports'].keys()))
        }

        for port_spec in link_network['Ports']:
            port = port_spec.split('/')[0]
            link_env.update({
                '{}_PORT_{}'.format(link_name, port): port
            })
        return link_env

    # NOTE Consul should provide a more efficient way to do that
    @factory.safe_docker
    def discover(self, link_name):
        '''
        Search for the given service and update its environment with
        connection informations
        '''
        link_node = self.dock.inspect_container(link_name)

        link_env = self._build_link_env(
            link_name, link_node['NetworkSettings']
        )
        self.environment.update(link_env)
        self.links.append(link_env)

    def synthetize(self, profile, gene, data=None):
        ''' Apply the given saltstack state on the current image '''
        data = data or {}
        self.state.switch_context(profile, self.name)
        self.state.store_data(profile, data)
        cmd = 'state.sls' if gene in self.state.library else 'cmd.run'
        return self.state.call([cmd], self.name, args=[[gene]])
