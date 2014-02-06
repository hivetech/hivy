#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2014 xavier <xavier@laptop-300E5A>


import salt.client
import docker
from flask.ext import restful


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

    local = salt.client.LocalClient()
    dock = docker.Client(base_url='unix://var/run/docker.sock',
                         version='0.7.6',
                         timeout=10)

    def __init__(self, image, name):
        self.image = image
        self.name = name

    def check(self, servers):
        ''' Check if servers are up '''
        return self.local.cmd(servers, 'test.ping')

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
            'running': False}


class RestNode(restful.Resource):

    # TODO Get this information from authentification
    default_username = 'chuck'
    default_image = 'hivetech/prototype'

    # NOTE Instanciate Node in the constructor is ok because there is one image
    # and one user. But what about later with several of both ?
    def __init__(self):
        self.node = Node(self.default_image,
                         self._node_name(self.default_username))

    def _node_name(self, username):
        return '{}-lab'.format(username)

    def get(self):
        return self.node.describe()

    def post(self):
        return self.node.activate()

    def delete(self):
        return self.node.destroy()
