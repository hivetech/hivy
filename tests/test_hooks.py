#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import unittest
import os

import hivy.reactor.hooks.utils as hooksutils


class HookUtilsTestCase(unittest.TestCase):

    def setUp(self):
        self.hook_name = 'debug'
        self.hook_role = 'tests'
        self.hook_event = 'member-join'
        self.debug_log_file = '/tmp/hook.log'
        os.environ = {
            'SERF_SELF_NAME': self.hook_name,
            'SERF_SELF_ROLE': self.hook_role,
            'SERF_EVENT': self.hook_event,
        }

        self.debug_hook = hooksutils.Debug()

    def tearDown(self):
        if os.path.exists(self.debug_log_file):
            os.remove(self.debug_log_file)

    def test_dump_context(self):
        self.debug_hook._dump_context()
        self.assertTrue(os.path.exists(self.debug_log_file))
        with open(self.debug_log_file, 'r') as fd:
            content = fd.read()
            for info in [self.hook_name, self.hook_role, self.hook_event]:
                info = info.replace('-', '_')
                self.assertTrue(info in content)

    def test_alias_methods(self):
        self.debug_hook.deploy()
        self.debug_hook.member_join()
        self.debug_hook.member_leave()
        self.debug_hook.member_failed()
        self.debug_hook.member_update()
        with open(self.debug_log_file, 'r') as fd:
            content = fd.read()
            self.assertTrue(content.count(self.hook_name) == 5)
