# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2014 Hive Tech, SAS.


import hivy.resources.system as system
import hivy.resources.node as node
import hivy.utils as utils
import hivy.reactor.hooks.utils as hooksutils


ROUTES = {
    '/': system.Status,
    utils.api_url('doc'): system.Doc,
    utils.api_url('node'): node.RestNode
}

HOOKS = {
    'lab': hooksutils.Debug
}

LOGFILE = '/tmp/hivy.log'
LOG_FORMAT = (u'[{record.time:%m-%d %H:%M}] '
              '{record.level_name}.{record.channel} {record.message}')


SERVER_URL = 'http://unide.co'
