#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


#import salt.client
import os
import docker
from flask.ext import restful
import flask

import hivy.auth as auth


class Node:
    '''
    Basic primitive of the infrastructure.
    Nodes are basically containers with high level methods for abstraction and
    easy management.

    salt-master must run as the same user as this script (usually system user)
    Change in /etc/salt/master:
      - user: username
      - root_dir: /home/username
    '''

    #local = salt.client.LocalClient()

    def __init__(self, image, name):
        self.image = image
        self.name = name

        docker_url = os.environ.get('DOCKER_URL', 'unix://var/run/docker.sock')
        self.dock = docker.Client(base_url=docker_url,
                                  version='0.7.6',
                                  timeout=10)

    #TODO Detection salt master ip
    def _salt_master_ip(self):
        return os.environ.get('SALT_MASTER_URL', 'localhost')

    def check(self, servers):
        ''' Check if servers are up '''
        #return self.local.cmd(servers, 'test.ping')
        return {'localhost': 'ok'}

    def activate(self):
        try:
            feedback = self.dock.create_container(
                self.image,
                detach=True,
                environment={
                    'SALT_MASTER': self._salt_master_ip(),
                    'NODE_ID': self.name,
                    'NODE_ROLE': 'lab'},
                hostname=self.name,
                name=self.name)
            feedback.update({'name': self.name})
            self.dock.start(self.feedback['Id'])
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
                'ip': '',
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
                    'hostname': node['Config']['Hostname']
                },
                'acl': [],
                'links': []}
        except docker.APIError, error:
            infos = {'error': str(error)}

        return infos


class RestNode(restful.Resource):

    method_decorators = [auth.requires_token_auth]
    default_image = os.environ.get('NODE_IMAGE', 'quay.io/hackliff/node')

    def _node_name(self):
        return '{}-lab'.format(flask.g.get('user'))

    def get(self):
        return Node(self.default_image, self._node_name()).inspect()

    def post(self):
        return Node(self.default_image, self._node_name()).activate()

    def delete(self):
        return Node(self.default_image, self._node_name()).destroy()
