#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.
# Distributed under terms of the MIT license.


import unittest
import time

import hivy.app as app
from hivy.node import Node


#TODO Test RestNode._node_name()
class RestNodeTestCase(unittest.TestCase):

    default_user = 'chuck'

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_get_node_informations(self):
        infos = self.app.get('/node')
        assert 'id' in infos.data

    def test_create_node(self):
        # Wait for the container to be correctly started
        time.sleep(2)
        feedback = self.app.post('/node')
        assert 'error' not in feedback.data
        assert feedback.data

    def test_delete_node(self):
        feedback = self.app.delete('/node')
        assert 'error' not in feedback.data
        assert feedback.data


class NodeTestCase(unittest.TestCase):

    servers_test = '*'
    name_test = 'chuck-lab'
    image_test = 'hivetech/prototype'

    def setUp(self):
        self.node = Node(self.image_test, self.name_test)

    '''
    def test_check(self):
        report = self.node.check(self.servers_test)
        assert report
        assert report['home']
    '''

    def test_describe_node(self):
        description = self.node.describe()
        assert 'id' in description

    def test_activate_node(self):
        feedback = self.node.activate()
        assert 'error' not in feedback
        assert feedback

    def test_destroy_node(self):
        # Wait for the container to be correctly started
        time.sleep(2)
        feedback = self.node.destroy()
        assert 'error' not in feedback
        assert feedback
