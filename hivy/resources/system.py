# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  system resource
  ---------------

  Expose Hivy server informations

  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''

import os
import flask
from flask.ext import restful
import dna.logging
import dna.utils
from hivy import __version__
import hivy.utils as utils
import hivy.reactor.reactor as reactor
from hivy.genetics.saltstack import Saltstack
from hivy.resources.node import RestfulNode

log = dna.logging.logger(__name__)


class Status(restful.Resource):
    ''' Expose Hivy services states and versions '''

    def __init__(self):
        self.hivy_version = dna.utils.Version(__version__)
        self.serf = reactor.Serf()
        self.salt = Saltstack()

    def get(self):
        ''' Inspect Hivy, docker, salt-master and serf states '''
        log.info('request hivy status')
        docker_version, docker_status = utils.docker_check()

        return flask.jsonify({
            'state': {
                'hivy': os.environ.get('HIVY_STATUS', True),
                'sub-systems': {
                    'docker': docker_status,
                    'salt-master': utils.is_running('salt-master'),
                    'serf': utils.is_running('serf')
                }
            },
            'version': {
                'hivy': {
                    'major': self.hivy_version.major,
                    'minor': self.hivy_version.minor,
                    'patch': self.hivy_version.patch
                },
                'docker': docker_version,
                'serf': self.serf.version(),
                #'salt': str(self.salt('--version'))
                'salt': self.salt.version()
            }
        })


class Doc(restful.Resource):
    ''' Expose last api documentation '''

    def get(self):
        ''' Expose doc on GET /v0/doc '''
        log.info('request hivy doc')
        return flask.jsonify({
            'api': {
                'GET /': Status.__doc__,
                utils.api_doc('doc', 'GET'): Doc.__doc__,
                utils.api_doc(
                    'node/<string:image>',
                    'GET | POST | DELETE',
                    cpu=2, ram=512): RestfulNode.__doc__
            }
        })
