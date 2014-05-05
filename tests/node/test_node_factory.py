# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import time
import unittest
from nose.tools import eq_, ok_
import dna.test_utils
import hivy.test_utils as test_utils
from hivy.node.factory import NodeFactory


class NodeFactoryTestCase(unittest.TestCase):

    def setUp(self):
        dna.test_utils.setup_logger(self)
        self.servers_test = '*'
        self.image_test = 'hivetech/base'
        self.name_test = 'test-node-factory'
        self.node = NodeFactory(
            self.image_test, self.name_test
        )

    def tearDown(self):
        dna.test_utils.teardown_logger(self)

    def test_initialize(self):
        eq_(self.node.links, [])
        eq_(self.node.environment,
            {'NODE_ID': self.name_test})

    @test_utils.module_required('docker')
    def test_inspect_absent_node(self):
        description = self.node.properties
        ok_('error' in description)

    @test_utils.module_required('docker')
    def test_activate_node(self):
        feedback = self.node.activate()
        ok_('error' not in feedback)
        ok_('Id' in feedback)
        ok_('name' in feedback)

    @test_utils.module_required('docker')
    def test_inspect_node(self):
        time.sleep(5)
        description = self.node.properties
        for info in ['ip', 'node', 'state', 'name']:
            self.assertTrue(info in description)

    @test_utils.module_required('docker')
    def test_destroy_node(self):
        # Wait for the container to be correctly started
        time.sleep(5)
        feedback = self.node.destroy()
        ok_('error' not in feedback)
        ok_('name' in feedback)
        ok_('destroyed' in feedback)
