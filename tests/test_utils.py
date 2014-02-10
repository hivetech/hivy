#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import unittest

import hivy.utils as utils


class UtilsTestCase(unittest.TestCase):

    def test_api_url(self):
        resource = 'node'
        formatted_url = utils.api_url(resource)
        self.assertTrue('/v' in formatted_url)
        self.assertTrue(resource in formatted_url)

    def _check_sub_version(self, sub_version):
        self.assertTrue(isinstance(sub_version, int))
        self.assertTrue(sub_version >= 0)
        self.assertTrue(sub_version < 10)

    def test_version_object(self):
        version = utils.Version()

        self._check_sub_version(version.major)
        self._check_sub_version(version.minor)
        self._check_sub_version(version.patch)
