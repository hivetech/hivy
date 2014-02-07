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

    def __init__(self, image, name):
        self.image = image
        self.name = name

        docker_url = os.environ.get('DOCKER_URL', 'unix://var/run/docker.sock')
        self.dock = docker.Client(base_url=docker_url,
                                  version='0.7.6',
                                  timeout=10)

    def check(self, servers):
        ''' Check if servers are up '''
        #return self.local.cmd(servers, 'test.ping')
        return {'localhost': 'ok'}

    def activate(self):
        #In [6]: print res
        #{u'Id': u'8d8c2cf070adda1...'}
        try:
            feedback = self.dock.create_container(
                self.image,
                detach=True,
                name=self.name)
            self.dock.start(feedback['Id'])
        except docker.APIError, error:
            feedback = {'error': error}
        return feedback

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
    default_image = 'hivetech/prototype'

    def _node_name(self):
        return '{}-lab'.format(flask.g.get('user'))

    def get(self):
        return Node(self.default_image, self._node_name()).describe()

    def post(self):
        return Node(self.default_image, self._node_name()).activate()

    def delete(self):
        return Node(self.default_image, self._node_name()).destroy()
