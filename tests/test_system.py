#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import os
import unittest

from hivy.app import app
from hivy import __api__


# http://flask.pocoo.org/docs/testing/
# http://packages.python.org/Flask-Testing/
class SystemTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.serf_ready = os.environ.get('SERF_READY')

    def test_get_status(self):
        res = self.app.get('/')
        for service in ['hivy', 'docker', 'serf', 'salt']:
            self.assertTrue(service in res.data)

    def test_get_version(self):
        if self.serf_ready:
            res = self.app.get('/version')
            for info in ['major', 'minor', 'patch']:
                self.assertTrue(info in res.data)
            for service in ['docker', 'salt', 'serf']:
                self.assertTrue(service in res.data)
        else:
            pass

    def test_get_global_doc(self):
        res = self.app.get('/v0/doc')
        assert res.data == '{"api": %s}' % str(__api__).replace('\'', '"')
