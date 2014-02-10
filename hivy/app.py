#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2014 Hive Tech, SAS.


'''Hivy

Usage:
  hivy -h | --help
  hivy --version
  hivy [--bind=<ip>] [--port=<port>] [-d | --debug]

Options:
  -h --help       Show this screen.
  --version       Show version.
  --debug         Activates Flask debug
  --bind=<ip>     Listens on the given ip [default: 127.0.0.1]
  --port=<port>   Listens on the given port [default: 5000]
'''


from flask import Flask, request
from flask.ext import restful
from docopt import docopt

import hivy.resources.system as system
import hivy.resources.node as node
import hivy.utils as utils


app = Flask(__name__)
app.config.update(
    PROPAGATE_EXCEPTIONS=False,
    PRESERVE_CONTEXT_ON_EXCEPTION=True
)

api = restful.Api(app)
api.add_resource(system.Status, '/')
api.add_resource(system.Version, '/version')
api.add_resource(system.Doc, utils.api_url('doc'))
api.add_resource(node.RestNode, utils.api_url('node'))


#TODO Use it for logging and perfs
@app.before_request
def before_request():
    print request


@app.after_request
def after_request(response):
    print response
    return response


if __name__ == '__main__':
    args = docopt(__doc__, version='Hivy, Hive api 0.0.3')

    app.run(host=args['--bind'],
            port=int(args['--port']),
            debug=args['--debug'])
