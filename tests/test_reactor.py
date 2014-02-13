#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import os
import unittest

import hivy.reactor.reactor as reactor


class SerfTestCase(unittest.TestCase):

    serf_ready = os.environ.get('SERF_READY')
    docker_ready = os.environ.get('DOCKER_READY')
    wrong_ip = '1.2.3.4'

    def setUp(self):
        self.serf = reactor.Serf()

    def test_serf_version(self):
        version = self.serf.version()
        self.assertTrue(len(version) == 2)
        self.assertTrue('Serf' in version[0])
        self.assertTrue('Agent Protocol' in version[1])

    def test_valid_serf_version(self):
        version = self.serf.version()
        minor_version = int(version[0].split('.')[1])
        self.assertTrue(minor_version >= 4)
        protocol_version = int(version[1].split()[2])
        self.assertTrue(protocol_version >= 3)

    def test_detect_running_agent(self):
        if self.serf_ready:
            is_running = self.serf._ready()
            self.assertTrue(is_running)
        else:
            pass

    def test_detect_absent_agent(self):
        is_running = self.serf._ready()
        self.assertFalse(is_running)

    def test_command_failed_without_agent(self):
        if self.serf_ready:
            feedback, flag = self.serf._serf_command('join', self.wrong_ip)
            self.assertFalse(flag)
            self.assertTrue('no local agent' in feedback)
        else:
            pass

    def test_register_node(self):
        #FIXME to make this test to work we need:
        #   * A running local serf agent
        #   * A running lab
        #   * Its ip
        if self.serf_ready and self.docker_ready:
            right_ip = '172.17.0.9'
            feedback, flag = self.serf.register_node(right_ip)
            self.assertTrue(flag)
            self.assertTrue('Successfully' in feedback)
        else:
            pass

    def test_register_absent_node(self):
        #FIXME We need a running agent here as well
        if self.serf_ready:
            feedback, flag = self.serf.register_node(self.wrong_ip)
            self.assertFalse(flag)
            self.assertTrue('Error' in feedback)
        else:
            pass
