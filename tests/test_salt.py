# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import unittest
import os
import yaml
import hivy.test as test
from hivy.genetics.saltstack import Saltstack


class SaltTestCase(unittest.TestCase):

    minion_name_test = 'home'
    user_test = 'chuck'
    other_user_test = 'gekko'
    repository_test = 'hivetech/hivy'

    def setUp(self):
        os.environ.update({'SALT_DATA': '/tmp'})
        self.salt = Saltstack()

    @test.salt_required
    def test_cmd_run(self):
        result = self.salt._run('test.ping', self.minion_name_test)
        self.assertTrue(result == {self.minion_name_test: True})

    @test.salt_required
    def test_read_config(self):
        self.assertTrue(self.salt.config)
        self.assertTrue(self.salt.config['renderer'] == 'yaml_jinja')
        self.assertTrue(self.salt.config['interface'] == '0.0.0.0')

    @test.salt_required
    def test_read_pillar(self):
        data = self.salt._read_pillar(self.minion_name_test)
        self.assertTrue(self.minion_name_test in data)
        self.assertTrue(data[self.minion_name_test])
        self.assertTrue(
            data[self.minion_name_test]['repository'] == self.repository_test)

    @test.salt_required
    def test_debug_state(self):
        #FIXME cannot remove /tmp/hivy directory and date_* files
        result = self.salt._run(
            'state.sls', self.minion_name_test, ['debug'])
        self.assertTrue(os.path.exists('/tmp/date_csv.csv'))
        self.assertTrue(os.path.exists('/tmp/hivy'))

        self.assertTrue(self.minion_name_test in result)
        for _, feedback in result[self.minion_name_test].iteritems():
            self.assertTrue(feedback['result'])

    def test_switch_user_context(self):
        top_file = '/'.join(
            [self.salt.root_data, 'pillar', 'top.sls'])
        self.salt.switch_context(self.user_test, self.minion_name_test)
        self.assertTrue(os.path.exists(top_file))
        with open(top_file, 'r') as top_fd:
            content = yaml.load(top_fd.read())
        self.assertTrue(
            content['base'][self.minion_name_test][-1] == self.user_test)

    def test_store_pillar_data(self):
        pillar_file = '/'.join(
            [self.salt.root_data,
             'pillar', '{}.sls'.format(self.user_test)])
        useless_data = {'hello': 'world'}
        self.salt.store_data(self.user_test, useless_data)
        self.assertTrue(os.path.exists(pillar_file))
        with open(pillar_file, 'r') as pillar_fd:
            content = yaml.load(pillar_fd.read())
        self.assertTrue(content['hello'] == 'world')

    def test_detect_master_ip(self):
        # TODO Should be equal to local ip
        ip = self.salt._master_ip()
        self.assertTrue(ip)
