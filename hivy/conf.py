# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  API routes
  ----------

  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''

import dna.apy.resources
import hivy.resources.system as system
import hivy.resources.node as node
import hivy.utils as utils


ROUTES = {
    '/': system.Status,
    utils.api_url('doc'): system.Doc,
    utils.api_url('user/<string:username>'): dna.apy.resources.User,
    utils.api_url('nodes'): node.Fleet,
    utils.api_url('node/<string:image>'): node.RestfulNode
}
