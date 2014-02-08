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


class Node():
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
    container = None

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
            self.container = self.dock.create_container(
                self.image,
                detach=True,
                environment={'SALT_MASTER': self._salt_master_ip()},
                hostname=self.name,
                name=self.name)
            self.dock.start(self.container['Id'])
        except docker.APIError, error:
            self.container = {'error': error}

        return self.container

    def destroy(self):
        try:
            self.dock.stop(self.name)
            self.dock.remove_container(self.name)
            return {self.name: True}
        except docker.APIError, error:
            return {'error': error}

    def describe(self):
        #TODO Get useful informations
        return {
            'name': self.name,
            'id': 'zrbbnrberrber',
            'state': 'running',
            'acl': [],
            'links': []}


class RestNode(restful.Resource):

    method_decorators = [auth.requires_token_auth]
    default_image = os.environ.get('NODE_IMAGE', 'hackliff/lab')

    def _node_name(self):
        return '{}-lab'.format(flask.g.get('user'))

    def get(self):
        return Node(self.default_image, self._node_name()).describe()

    def post(self):
        return Node(self.default_image, self._node_name()).activate()

    def delete(self):
        return Node(self.default_image, self._node_name()).destroy()
