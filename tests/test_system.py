#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import unittest

from hivy.app import app
from hivy import __api__, SERF_ON


# http://flask.pocoo.org/docs/testing/
# http://packages.python.org/Flask-Testing/
class SystemTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_status(self):
        res = self.app.get('/')
        #TODO Check res['status']['docker'] == DOCKER_ON
        for service in ['hivy', 'docker', 'serf', 'salt']:
            self.assertTrue(service in res.data)

    def test_get_version(self):
        if SERF_ON:
            res = self.app.get('/')
            for info in ['major', 'minor', 'patch']:
                self.assertTrue(info in res.data)
            for service in ['docker', 'salt', 'serf']:
                self.assertTrue(service in res.data)
        else:
            pass

    def test_get_v0_doc(self):
        res = self.app.get('/v0/doc')
        assert res.data == '{"api": %s}' % str(__api__).replace('\'', '"')
