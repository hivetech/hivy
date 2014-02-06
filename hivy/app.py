#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2014 xavier <xavier@laptop-300E5A>


'''Hive api

Usage:
  api -h | --help
  api --version
  api [--bind=<ip>] [--port=<port>] [-d | --debug]

Options:
  -h --help       Show this screen.
  --version       Show version.
  --debug         Activates Flask debug
  --bind=<ip>     Listens on the given ip [default: 127.0.0.1]
  --port=<port>   Listens on the given port [default: 5000]
'''


from flask import Flask
from flask.ext import restful
from docopt import docopt

import hivy.system as system
import hivy.node as node


app = Flask(__name__)
app.config.update(
    PROPAGATE_EXCEPTIONS=False,
    PRESERVE_CONTEXT_ON_EXCEPTION=True
)

api = restful.Api(app)
api.add_resource(system.Status, '/')
api.add_resource(system.Version, '/version')
api.add_resource(system.Doc, '/doc')
api.add_resource(node.RestNode, '/node')


if __name__ == '__main__':
    args = docopt(__doc__, version='Hivy, Hive api 0.0.1')

    app.run(host=args['--bind'],
            port=int(args['--port']),
            debug=args['--debug'])
