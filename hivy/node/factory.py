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

import abc
import docker
import hivy.settings
import dna.logging

log = dna.logging.logger(__name__)


class NodeFactory(object):
    '''
    Basic abstract primitive of the infrastructure.
    Nodes are basically containers with high level methods for abstraction and
    easy management.
    '''

    __metaclass__ = abc.ABCMeta

    builtin_ports = {22: None}
    links = []

    def __init__(self, image, name, role,
                 docker_url=hivy.settings.DEFAULT_DOCKER_URL):
        log.info('initiating node', image=image, name=name, role=role)
        self.image = image
        self.name = name
        self.role = role
        self.environment = {
            'NODE_ID': name,
            'NODE_ROLE': role
        }

        # TODO version and timeout not hardcoded
        log.info('connecting to docker server',
                 url=docker_url, version='0.7.6', timeout=10)
        self.dock = docker.Client(
            base_url=docker_url, version='0.7.6', timeout=10)

    def activate(self, ports=[], extra_env={}):
        ''' Create a new docker container from an existing image '''
        try:
            exposed_ports = self.builtin_ports
            exposed_ports.update({port: None for port in ports})
            self.environment.update(extra_env)
            feedback = self.dock.create_container(
                self.image,
                detach=True,
                hostname=self.name,
                name=self.name,
                ports=exposed_ports.keys(),
                environment=self.environment,
                command=['/sbin/my_init', '--enable-insecure-key']
            )
            feedback.update({'name': self.name})

            # NOTE Should use publish_all_ports instead ?
            self.dock.start(feedback['Id'], port_bindings=exposed_ports)
            log.info('activated node',
                     image=self.image, name=self.name,
                     env=self.environment, feedback=feedback)
        except docker.APIError, error:
            feedback = {'error': str(error)}
            log.error('node activation failed', error=error)

        return feedback

    def destroy(self):
        ''' Stop and remove the container '''
        try:
            self.dock.stop(self.name)
            self.dock.remove_container(self.name)
            feedback = {
                'name': self.name,
                'destroyed': True}
            log.info('node destroyed', feedback=feedback)
        except docker.APIError, error:
            log.error('node destruction failed', error=error)
            feedback = {'error': str(error)}
        return feedback

    def inspect(self):
        ''' Fetch container relevant informations for the user '''
        try:
            node = self.dock.inspect_container(self.name)
            infos = {
                'name': self.name,
                'ip': '{}:{}'.format(
                    hivy.settings.SERVER_URL,
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
                'links': self.links}
            log.info('inspected node', infos=infos)
        except docker.APIError, error:
            log.error('node inspection failed', error=error)
            infos = {'error': str(error)}

        return infos
