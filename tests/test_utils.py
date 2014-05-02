# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import yaml
import unittest
from nose.tools import eq_, ok_, nottest
import hivy.utils as utils


# TODO Test clean_request_data
class UtilsTestCase(unittest.TestCase):

    random_length = 64
    always_running_process = 'init'

    def test_api_url(self):
        resource = 'node'
        formatted_url = utils.api_url(resource)
        ok_('/v' in formatted_url)
        ok_(resource in formatted_url)

    def test_api_doc(self):
        doc = utils.api_doc('node', 'GET', key='value')
        eq_(doc, 'GET /v0/node?key=value')

    @nottest
    def _check_sub_version(self, sub_version):
        ok_(isinstance(sub_version, int))
        ok_(sub_version >= 0)
        ok_(sub_version < 10)

    def test_write_to_yaml_file(self):
        fake_data = {'test': {'fake': 'data'}}
        utils.write_yaml_data('/tmp/fake.yml', fake_data)
        ok_(os.path.exists('/tmp/fake.yml'))
        with open('/tmp/fake.yml', 'r') as fake_fd:
            content = yaml.load(fake_fd.read())
        eq_(content['test']['fake'], 'data')
        os.remove('/tmp/fake.yml')

    def test_to_utf8_dict_idempotent(self):
        eq_(utils.to_utf8_dict({}), {})
        eq_(utils.to_utf8_dict({'hello': 'world'}),
            {'hello': 'world'})

    def test_to_utf8_dict_from_unicode(self):
        eq_(utils.to_utf8_dict({unicode('hello'): unicode('world')}),
            {'hello': 'world'})
