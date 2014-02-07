#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


from hivy import __version__, __doc__
import hivy.app as app
import unittest


# http://flask.pocoo.org/docs/testing/
# http://packages.python.org/Flask-Testing/
class SystemTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_get_status(self):
        res = self.app.get('/')
        assert res.data == '{"status": "ok"}'

    def test_get_version(self):
        res = self.app.get('/version')
        assert res.data == '{"version": "%s"}' % __version__

    def test_get_global_doc(self):
        res = self.app.get('/doc')
        assert res.data == '{"doc": %s}' % str(__doc__).replace('\'', '"')
