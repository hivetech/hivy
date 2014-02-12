#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import hivy
import unittest


# http://flask.pocoo.org/docs/testing/
# http://packages.python.org/Flask-Testing/
class SystemTestCase(unittest.TestCase):

    def setUp(self):
        hivy.app.config['TESTING'] = True
        self.app = hivy.app.test_client()

    def tearDown(self):
        pass

    def test_get_status(self):
        res = self.app.get('/')
        for service in ['hivy', 'docker', 'serf', 'salt']:
            self.assertTrue(service in res.data)

    def test_get_version(self):
        res = self.app.get('/version')
        for info in ['major', 'minor', 'patch']:
            self.assertTrue(info in res.data)
        for service in ['docker', 'salt', 'serf']:
            self.assertTrue(service in res.data)

    def test_get_global_doc(self):
        res = self.app.get('/v0/doc')
        assert res.data == '{"api": %s}' % str(hivy.__api__).replace('\'', '"')
