#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import os
import unittest
import hivy.utils as utils
import hivy.test as test


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

    def test_hivy_version_object(self):
        version = utils.Version()

        self._check_sub_version(version.major)
        self._check_sub_version(version.minor)
        self._check_sub_version(version.patch)

    def test_running_process_detection(self):
        self.assertTrue(utils.is_running(self.always_running_process))

    def test_not_running_process_detection(self):
        self.assertFalse(utils.is_running('no_chance_this_program_is_running'))

    def test_subsystem_available_and_allowed(self):
        os.environ.update({'USE_{}'.format(
            self.always_running_process.upper()): True})
        is_available = utils.is_available(self.always_running_process)
        self.assertTrue(is_available)
        os.environ.pop('USE_{}'.format(self.always_running_process.upper()))

    def test_subsystem_available_but_not_allowed(self):
        is_available = utils.is_available(self.always_running_process)
        self.assertFalse(is_available)

    def test_subsystem_not_available_and_not_allowed(self):
        is_available = utils.is_available('program_not_running')
        self.assertFalse(is_available)

    def test_subsystem_not_available_but_allowed(self):
        os.environ.update({'USE_PROGRAM_NOT_RUNNING': True})
        is_available = utils.is_available('program_not_running')
        self.assertFalse(is_available)
        os.environ.pop('USE_PROGRAM_NOT_RUNNING')

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

    @test.docker_required
    def test_detect_docker_available(self):
        os.environ.update({'USE_DOCKER': True})
        is_available = utils.is_available('docker')
        self.assertTrue(is_available)
        os.environ.pop('USE_DOCKER')

    def test_handle_docker_not_available(self):
        #TODO with a wrong DOCKER_URL
        os.environ.update({'DOCKER_URL': 'http://1.2.3.4.:4243'})
        os.environ.update({'USE_DOCKER': True})
        is_available = utils.is_available('docker')
        self.assertFalse(is_available)
        os.environ.pop('USE_DOCKER')
        pass
