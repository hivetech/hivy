# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import time
import os
import unittest
import flask.ext.testing
from werkzeug.datastructures import Headers
import werkzeug.test
import apy.core
import hivy.conf
import hivy.test_utils as test_utils
from hivy.node.factory import NodeFactory
from hivy.node.foundation import NodeFoundation


# TODO Test RestNode._node_name()
class RestfulNodeTestCase(flask.ext.testing.TestCase):

    default_user = 'chuck'
    invalid_test_token = '4321'
    valid_test_token = 'd2a879423e53ddbb6788bbc286647a793440f3db'
    node_resource_path = '/v0/node/node'

    def create_app(self):
        app = apy.core.App(hivy.conf.ROUTES).app
        app.config['TESTING'] = True
        return app

    def test_node_resource_is_locked(self):
        rv = self.client.get(self.node_resource_path)
        self.assert_401(rv)
        self.assertTrue('WWW-Authenticate' in rv.headers)
        self.assertTrue('Token' in rv.headers['WWW-Authenticate'])

    def test_node_invalid_token_rejected(self):
        h = Headers()
        h.add('Authorization', self.invalid_test_token)
        rv = werkzeug.test.Client.open(
            self.client, path=self.node_resource_path, headers=h)
        self.assert_401(rv)

    @test_utils.docker_required
    def test_get_absent_node_informations(self):
        h = Headers()
        h.add('Authorization', self.valid_test_token)
        rv = self.client.get(self.node_resource_path, headers=h)
        self.assertTrue('error' in rv.data)

    @test_utils.docker_required
    def test_create_node(self):
        h = Headers()
        h.add('Authorization', self.valid_test_token)
        rv = self.client.post(self.node_resource_path, headers=h)
        assert 'error' not in rv.data
        assert 'Id' in rv.data
        assert 'name' in rv.data

    @test_utils.docker_required
    def test_get_existing_node_informations(self):
        time.sleep(5)
        h = Headers()
        h.add('Authorization', self.valid_test_token)
        rv = self.client.get(self.node_resource_path, headers=h)
        for info in ['ip', 'node', 'state', 'name']:
            self.assertTrue(info in rv.data)

    @test_utils.docker_required
    def test_delete_node(self):
        # Wait for the container to be correctly started
        time.sleep(5)
        h = Headers()
        h.add('Authorization', self.valid_test_token)
        rv = self.client.delete(self.node_resource_path, headers=h)
        assert 'error' not in rv.data
        assert 'name' in rv.data
        assert 'destroyed' in rv.data


class NodeFactoryTestCase(unittest.TestCase):

    servers_test = '*'
    image_test = os.environ.get('NODE_IMAGE', 'quay.io/hackliff/node')
    role_test = 'test'
    name_test = 'test-node-factory'

    def setUp(self):
        self.node = NodeFactory(
            self.image_test, self.name_test, self.role_test)

    @test_utils.docker_required
    def test_inspect_absent_node(self):
        description = self.node.inspect()
        assert 'error' in description

    @test_utils.docker_required
    def test_activate_node(self):
        feedback = self.node.activate()
        assert 'error' not in feedback
        assert 'Id' in feedback
        assert 'name' in feedback

    @test_utils.docker_required
    def test_inspect_node(self):
        time.sleep(5)
        description = self.node.inspect()
        for info in ['ip', 'node', 'state', 'name']:
            self.assertTrue(info in description)

    @test_utils.docker_required
    def test_destroy_node(self):
        # Wait for the container to be correctly started
        time.sleep(5)
        feedback = self.node.destroy()
        assert 'error' not in feedback
        assert 'name' in feedback
        assert 'destroyed' in feedback


class NodeFoundationTestCase(unittest.TestCase):

    image_test = os.environ.get('NODE_IMAGE', 'quay.io/hackliff/node')
    role_test = 'test'
    name_test = 'test-node-foundation'

    def setUp(self):
        self.node = NodeFoundation(
            self.image_test, self.name_test, self.role_test)

    @test_utils.docker_required
    @test_utils.serf_required
    def test_register_node(self):
        pass

    @test_utils.docker_required
    @test_utils.serf_required
    def test_forget_node(self):
        pass

    @test_utils.salt_required
    def test_synthetize(self):
        pass
