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
import abc
import docker
import hivy.settings
import dna.logging

log = dna.logging.logger(__name__)


def safe_docker(docker_command):
    ''' catch docker errors '''
    def inner(*args, **kwargs):
        try:
            feedback = docker_command(*args, **kwargs)
        # FIXME except docker.APIError, error:
        except Exception as error:
            feedback = {'error': str(error)}
            log.error('node action failed', error=str(error))
        return feedback
    return inner


class NodeFactory(object):
    '''
    Basic abstract primitive of the infrastructure.
    Nodes are basically containers with high level methods for abstraction and
    easy management.
    '''

    __metaclass__ = abc.ABCMeta

    # Enable ssh per default
    _builtin_ports = {22: None}
    # See https://github.com/phusion/passenger-docker
    _phusion_command = ['/sbin/my_init', '--enable-insecure-key']

    def __init__(self, image, name,
                 docker_url=hivy.settings.DEFAULT_DOCKER_URL):

        log.info('initiating node', image=image, name=name)
        self.image = image
        self.name = name
        self.environment = {
            'NODE_ID': name,
        }

        self.links = []
        # TODO version and timeout not hardcoded
        log.info('connecting to docker server', url=docker_url)
        self.dock = docker.Client(
            base_url=docker_url, version='0.7.6', timeout=10)

    def _build_container_attributes(self, exposed_ports):
        return {
            'image': self.image,
            'hostname': self.name,
            'name': self.name,
            'ports': exposed_ports.keys(),
            'environment': self.environment,
            'command': self._phusion_command,
            'detach': True
        }

    @safe_docker
    def activate(self, ports=None, extra_env=None):
        ''' Create a new docker container from an existing image '''
        ports = ports or []
        extra_env = extra_env or {}

        self.environment.update(extra_env)
        exposed_ports = self._builtin_ports
        exposed_ports.update({port: None for port in ports})
        properties = self._build_container_attributes(exposed_ports)

        feedback = self.dock.create_container(**properties)
        feedback.update({'name': self.name})

        # NOTE Should use publish_all_ports instead ?
        self.dock.start(feedback['Id'], port_bindings=exposed_ports)
        log.info('activated node',
                 image=self.image, name=self.name,
                 env=self.environment, feedback=feedback)

        return feedback

    @safe_docker
    def destroy(self):
        ''' Stop and remove the container '''
        self.dock.stop(self.name)
        log.info('node stopped')
        self.dock.remove_container(self.name)
        log.info('node destroyed')
        return {
            'name': self.name,
            'destroyed': True
        }

    @property
    @safe_docker
    def properties(self):
        ''' Fetch container relevant informations for the user '''
        node = self.dock.inspect_container(self.name)
        return {
            'name': self.name,
            'ip': ':'.join([
                os.environ.get('DOMAIN', 'api.unide.co'),
                node['NetworkSettings']['Ports']['22/tcp'][0]['HostPort']
            ]),
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
            'links': self.links
        }
