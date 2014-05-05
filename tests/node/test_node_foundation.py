# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import unittest
from nose.tools import eq_
import dna.test_utils
import hivy.test_utils as test_utils
from hivy.node.foundation import NodeFoundation


class NodeFoundationTestCase(unittest.TestCase):

    def setUp(self):
        dna.test_utils.setup_logger(self)
        self.image_test = 'hivetech/base'
        self.name_test = 'test-node-foundation'
        self.node = NodeFoundation(
            self.image_test, self.name_test)

    def tearDown(self):
        dna.test_utils.teardown_logger(self)

    def test_initialize(self):
        eq_(self.node.links, [])
        eq_(sorted(self.node.environment.keys()),
            sorted(['NODE_ID', 'SALT_MASTER', 'CONSUL_MASTER']))

    @test_utils.module_required('serf')
    def test_register_node(self):
        pass

    @test_utils.docker_required
    @test_utils.module_required('serf')
    def test_forget_node(self):
        pass

    @test_utils.module_required('salt')
    def test_synthetize(self):
        pass
