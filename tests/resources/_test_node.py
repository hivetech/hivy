# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import time
import flask.ext.testing
from werkzeug.datastructures import Headers
import werkzeug.test
import dna.apy.core
import hivy.conf
import hivy.test_utils as test_utils


# TODO Test RestNode._node_name()
class RestfulNodeTestCase(flask.ext.testing.TestCase):

    def create_app(self):
        application = dna.apy.core.Application
        application.setup_routes(hivy.conf.ROUTES)
        app = application.app
        app.config['TESTING'] = True
        self.client = app.test_client()
        return app

    def setUp(self):
        self.default_user = 'chuck'
        self.invalid_test_token = '4321'
        self.valid_test_token = 'd2a879423e53ddbb6788bbc286647a793440f3db'
        self.node_resource_path = '/v0/node/node'

    '''
    def test_node_resource_is_locked(self):
        rv = self.client.get(self.node_resource_path)
        self.assert_401(rv)
        ok_('WWW-Authenticate' in rv.headers)
        ok_('Token' in rv.headers['WWW-Authenticate'])
    '''

    def test_node_invalid_token_rejected(self):
        h = Headers()
        h.add('Authorization', self.invalid_test_token)
        rv = werkzeug.test.Client.open(
            self.client, path=self.node_resource_path, headers=h)
        self.assert_401(rv)

    @test_utils.module_required('docker')
    def test_get_absent_node_informations(self):
        h = Headers()
        h.add('Authorization', self.valid_test_token)
        rv = self.client.get(self.node_resource_path, headers=h)
        self.assertTrue('error' in rv.data)

    @test_utils.module_required('docker')
    def test_create_node(self):
        h = Headers()
        h.add('Authorization', self.valid_test_token)
        rv = self.client.post(self.node_resource_path, headers=h)
        assert 'error' not in rv.data
        assert 'Id' in rv.data
        assert 'name' in rv.data

    @test_utils.module_required('docker')
    def test_get_existing_node_informations(self):
        time.sleep(5)
        h = Headers()
        h.add('Authorization', self.valid_test_token)
        rv = self.client.get(self.node_resource_path, headers=h)
        for info in ['ip', 'node', 'state', 'name']:
            self.assertTrue(info in rv.data)

    @test_utils.module_required('docker')
    def test_delete_node(self):
        # Wait for the container to be correctly started
        time.sleep(5)
        h = Headers()
        h.add('Authorization', self.valid_test_token)
        rv = self.client.delete(self.node_resource_path, headers=h)
        assert 'error' not in rv.data
        assert 'name' in rv.data
        assert 'destroyed' in rv.data
