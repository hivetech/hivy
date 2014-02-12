# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2014 Hive Tech, SAS.


import hivy.resources.system as system
import hivy.resources.node as node
import hivy.utils as utils


routes = {
    '/': system.Status,
    '/version': system.Version,
    utils.api_url('doc'): system.Doc,
    utils.api_url('node'): node.RestNode
}
