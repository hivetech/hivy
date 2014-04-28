# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import unittest
import os
import yaml
import hivy.utils as utils


# TODO Test clean_request_data
class UtilsTestCase(unittest.TestCase):

    random_length = 64
    always_running_process = 'init'

    def test_api_url(self):
        resource = 'node'
        formatted_url = utils.api_url(resource)
        self.assertTrue('/v' in formatted_url)
        self.assertTrue(resource in formatted_url)

    def _check_sub_version(self, sub_version):
        self.assertTrue(isinstance(sub_version, int))
        self.assertTrue(sub_version >= 0)
        self.assertTrue(sub_version < 10)

    def test_write_to_yaml_file(self):
        fake_data = {'test': {'fake': 'data'}}
        utils.write_yaml_data('/tmp/fake.yml', fake_data)
        os.path.exists('/tmp/fake.yml')
        with open('/tmp/fake.yml', 'r') as fake_fd:
            content = yaml.load(fake_fd.read())
        self.assertTrue(content['test']['fake'] == 'data')
        os.remove('/tmp/fake.yml')
