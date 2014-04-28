# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import unittest
import apy.core
import hivy.conf
import hivy.test_utils as test_utils


# http://flask.pocoo.org/docs/testing/
# http://packages.python.org/Flask-Testing/
class SystemTestCase(unittest.TestCase):

    def setUp(self):
        app = apy.core.App(hivy.conf.ROUTES).app
        app.config['TESTING'] = True
        self.app = app.test_client()

    @test_utils.consul_required
    def test_get_status(self):
        res = self.app.get('/')
        # TODO Check res['status']['docker'] == DOCKER_ON
        for service in ['hivy', 'docker', 'consul', 'salt']:
            self.assertTrue(service in res.data)

    @test_utils.consul_required
    def test_get_version(self):
        res = self.app.get('/')
        for info in ['major', 'minor', 'patch']:
            self.assertTrue(info in res.data)
        for service in ['docker', 'salt', 'consul']:
            self.assertTrue(service in res.data)

    def test_get_v0_doc(self):
        res = self.app.get('/v0/doc')
        for field in ['doc', 'api', 'node']:
            self.assertIn(field, res.data)
