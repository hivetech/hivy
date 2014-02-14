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
import docker
from hivy import SERVER_URL


class NodeFactory(object):
    '''
    Basic primitive of the infrastructure.
    Nodes are basically containers with high level methods for abstraction and
    easy management.
    '''

    def __init__(self, image, name, role):
        self.image = image
        self.name = name
        self.role = role

        docker_url = os.environ.get('DOCKER_URL', 'unix://var/run/docker.sock')
        self.dock = docker.Client(
            base_url=docker_url, version='0.7.6', timeout=10)
        self.environment = {
            'NODE_ID': self.name,
            'NODE_ROLE': self.role
        }

    def activate(self):
        try:
            feedback = self.dock.create_container(
                self.image,
                detach=True,
                hostname=self.name,
                name=self.name,
                ports=[22],
                environment=self.environment
            )
            feedback.update({'name': self.name})
            self.dock.start(feedback['Id'], port_bindings={22: None})
        except docker.APIError, error:
            feedback = {'error': str(error)}

        return feedback

    def destroy(self):
        try:
            self.dock.stop(self.name)
            self.dock.remove_container(self.name)
            return {
                'name': self.name,
                'destroyed': True}
        except docker.APIError, error:
            return {'error': str(error)}

    def inspect(self):
        try:
            node = self.dock.inspect_container(self.name)
            infos = {
                'name': self.name,
                'ip': '{}:{}'.format(
                    SERVER_URL,
                    node['NetworkSettings']['Ports']['22/tcp'][0]['HostPort']),
                'state': node['State'],
                'node': {
                    'created': node['Created'],
                    'id': node['ID'],
                    'env': node['Config']['Env'],
                    'cpu': node['Config']['CpuShares'],
                    'memory': node['Config']['Memory'],
                    'memory_swap': node['Config']['MemorySwap'],
                    'image': node['Config']['Image'],
                    'ports': node['HostConfig']['PortBindings'],
                    'virtual_ip': node['NetworkSettings']['IPAddress'],
                    'hostname': node['Config']['Hostname']
                },
                'acl': [],
                'links': []}
        except docker.APIError, error:
            infos = {'error': str(error)}

        return infos
