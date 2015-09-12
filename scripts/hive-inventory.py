#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Ansible dynamic inventory for the hive
  --------------------------------------

  Inspired from https://raw.githubusercontent.com/ansible/ansible/devel/plugins
      /inventory/ec2.py
  And http://docs.ansible.com/developing_inventory.html

  :copyright (c) 2014 Xavier Bruhiere.
  :license: Apache 2.0, see LICENSE for more details.
'''

import re
import argparse
import pyconsul.http
try:
    import json
except ImportError:
    import simplejson as json


class FactoryInventory(object):

    def _empty_inventory(self):
        return {"_meta": {"hostvars": {}}}

    def __init__(self):
        # Inventory grouped by instance IDs, tags, security groups, regions,
        # and availability zones
        self.inventory = self._empty_inventory()

        # Index of hostname (address) to instance ID
        self.index = {}

        # Read settings and parse CLI arguments
        self.parse_cli_args()

    def parse_cli_args(self):
        ''' Command line argument processing '''

        parser = argparse.ArgumentParser(
            description='Produce an Ansible Inventory file based on EC2'
        )
        parser.add_argument('--list', action='store_true', default=True,
                            help='List instances (default: True)')
        parser.add_argument('--host', action='store',
                            help='Get variables about a specific instance')
        self.args = parser.parse_args()

    def json_format_dict(self, data, pretty=False):
        ''' Converts a dict to a JSON object and dumps it as a formatted
        string '''
        if pretty:
            return json.dumps(data, sort_keys=True, indent=2)
        else:
            return json.dumps(data)

    def to_safe(self, word):
        ''' Converts 'bad' characters in a string to underscores so they can be
        used as Ansible groups '''
        return re.sub("[^A-Za-z0-9\-]", "_", word)

    def _safe_push(self, key, element):
        ''' Pushed an element onto an array that may not have been defined in
        the dict '''
        key = self.to_safe(key)

        if key in self.inventory:
            self.inventory[key].append(element)
        else:
            self.inventory[key] = [element]

    def output(self):
        if self.args.host:
            # TODO Return vars config for `host`
            return {'mode': 'prototype'}
        elif self.args.list:
            return self.json_format_dict(self.inventory, pretty=True)


class HiveInventory(FactoryInventory):

    def __init__(self):
        FactoryInventory.__init__(self)
        # Assume local consul for now
        self._hive = pyconsul.http.Consul()

    def inspect_hive(self):
        # Global tag
        for node in self._hive.nodes:
            self._safe_push('hive', node['Address'])
            self.inventory["_meta"]["hostvars"][node['Address']] = {}


if __name__ == '__main__':
    inventory_ = HiveInventory()
    inventory_.inspect_hive()
    print inventory_.output()
