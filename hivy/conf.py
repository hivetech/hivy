# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  API configuration
  -----------------

  Specify here restful routes and event hooks

  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''


import hivy.resources.system as system
import hivy.resources.node as node
import hivy.utils as utils
import hivy.reactor.hooks.utils as hooksutils


ROUTES = {
    '/': system.Status,
    utils.api_url('doc'): system.Doc,
    utils.api_url('node/<string:image>'): node.RestfulNode
}

HOOKS = {
    'node': hooksutils.Debug
}
