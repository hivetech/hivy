#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import time
import os
import unittest
from flask.ext.testing import TestCase
from werkzeug.datastructures import Headers
from werkzeug.test import Client

import hivy.app as app
from hivy.resources.node import Node


#TODO Test RestNode._node_name()
class RestNodeTestCase(TestCase):

    default_user = 'chuck'
    invalid_test_token = '4321'
    valid_test_token = '1234'
    docker_ready = os.environ.get('DOCKER_READY')

    def create_app(self):
        application = app.app
        application.config['TESTING'] = True
        return application

    def test_node_resource_is_locked(self):
        rv = self.client.get('/node')
        self.assert_401(rv)
        self.assertTrue('WWW-Authenticate' in rv.headers)
        self.assertTrue('Token' in rv.headers['WWW-Authenticate'])

    def test_node_invalid_token_rejected(self):
        h = Headers()
        h.add('Authorization', self.invalid_test_token)
        rv = Client.open(self.client, path='/node', headers=h)
        self.assert_401(rv)

    def test_get_node_informations(self):
        h = Headers()
        h.add('Authorization', self.valid_test_token)
        rv = self.client.get('/node', headers=h)
        self.assertTrue('id' in rv.data)
        self.assertTrue(self.default_user in rv.data)
        self.assertTrue('state' in rv.data)

    def test_create_node(self):
        if self.docker_ready:
            h = Headers()
            h.add('Authorization', self.valid_test_token)
            rv = self.client.post('/node', headers=h)
            assert 'error' not in rv.data
            assert rv.data
        else:
            pass

    def test_delete_node(self):
        if self.docker_ready:
            # Wait for the container to be correctly started
            time.sleep(5)
            h = Headers()
            h.add('Authorization', self.valid_test_token)
            rv = self.client.delete('/node', headers=h)
            assert 'error' not in rv.data
            assert rv.data
        else:
            pass


class NodeTestCase(unittest.TestCase):

    servers_test = '*'
    name_test = 'chuck-lab'
    image_test = 'hivetech/prototype'
    docker_ready = os.environ.get('DOCKER_READY')

    def setUp(self):
        self.node = Node(self.image_test, self.name_test)

    # Avoiding salt dependency for now
    #def test_check(self):
        #report = self.node.check(self.servers_test)
        #assert report
        #assert report['home']

    def test_describe_node(self):
        description = self.node.describe()
        assert 'id' in description

    def test_activate_node(self):
        if self.docker_ready:
            feedback = self.node.activate()
            assert 'error' not in feedback
            assert feedback
        else:
            pass

    def test_destroy_node(self):
        if self.docker_ready:
            # Wait for the container to be correctly started
            time.sleep(5)
            feedback = self.node.destroy()
            assert 'error' not in feedback
            assert feedback
        else:
            pass
