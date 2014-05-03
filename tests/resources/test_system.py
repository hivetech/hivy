# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import unittest
from nose.tools import ok_
import dna.apy.core
import hivy.conf
import hivy.test_utils as test_utils


# http://flask.pocoo.org/docs/testing/
# http://packages.python.org/Flask-Testing/
class SystemTestCase(unittest.TestCase):

    def setUp(self):
        application = dna.apy.core.Application
        application.setup_routes(hivy.conf.ROUTES)
        app = application.app
        app.config['TESTING'] = True
        self.app = app.test_client()

    @test_utils.module_required('consul')
    def test_get_status(self):
        res = self.app.get('/')
        # TODO Check res['status']['docker'] == DOCKER_ON
        for service in ['hivy', 'docker', 'consul', 'salt']:
            ok_(service in res.data)

    @test_utils.module_required('consul')
    def test_get_version(self):
        res = self.app.get('/')
        for info in ['major', 'minor', 'patch']:
            ok_(info in res.data)
        for service in ['docker', 'salt', 'consul']:
            ok_(service in res.data)

    def test_get_v0_doc(self):
        res = self.app.get('/v0/docs')
        for field in ['doc', 'api', 'node']:
            self.assertIn(field, res.data)
