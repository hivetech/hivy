#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import unittest
import os
import yaml
import hivy.utils as utils
#import hivy.test as test


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

    def test_running_process_detection(self):
        self.assertTrue(utils.is_running(self.always_running_process))

    def test_not_running_process_detection(self):
        self.assertFalse(utils.is_running('no_chance_this_program_is_running'))

    def test_generate_name(self):
        new_name = utils.generate_random_name()
        #TODO Regex validation
        self.assertTrue(isinstance(new_name, str))
        new_name = utils.generate_random_name(size=4)
        self.assertTrue(len(new_name) == 4)

    def test_id_generator(self):
        new_id = utils.generate_unique_id()
        self.assertTrue(isinstance(new_id, str))
        self.assertTrue(len(new_id) == 36)

    def test_id_generator_unicity(self):
        new_id = utils.generate_unique_id()
        for _ in range(self.random_length):
            old_id = new_id
            new_id = utils.generate_unique_id()
            self.assertTrue(new_id != old_id)

    def test_write_to_yaml_file(self):
        fake_data = {'test': {'fake': 'data'}}
        utils.write_yaml_data('/tmp/fake.yml', fake_data)
        os.path.exists('/tmp/fake.yml')
        with open('/tmp/fake.yml', 'r') as fake_fd:
            content = yaml.load(fake_fd.read())
        self.assertTrue(content['test']['fake'] == 'data')
        os.remove('/tmp/fake.yml')
