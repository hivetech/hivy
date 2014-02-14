#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import unittest

import hivy.test as test
import hivy.utils as utils


class UtilsTestCase(unittest.TestCase):

    def test_docker_required(self):
        @test.docker_required
        def dummy():
            return 'dummy_value'
        if utils.is_available('docker'):
            self.assertTrue(dummy() == 'dummy_value')
        else:
            self.assertFalse(dummy())

    def test_serf_required(self):
        @test.serf_required
        def dummy():
            return 'dummy_value'
        if utils.is_available('serf'):
            self.assertTrue(dummy() == 'dummy_value')
        else:
            self.assertFalse(dummy())

    def test_serf_and_docker_required(self):
        @test.serf_required
        @test.docker_required
        def dummy():
            return 'dummy_value'
        if utils.is_available('serf') and \
                utils.is_available('docker'):
            self.assertTrue(dummy() == 'dummy_value')
        else:
            self.assertFalse(dummy())
