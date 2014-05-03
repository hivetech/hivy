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
import dna.apy.resources
import hivy.utils
import hivy.genetics.saltstack as saltstack
from hivy.resources.node import RestfulNode, Fleet
from hivy.resources.proxy import RestfulHipache
import pyconsul.http


class Status(restful.Resource):
    ''' Expose Hivy services states and versions '''

    def __init__(self):
        self.hivy_version = dna.utils.Version(hivy.__version__)
        # NOTE Assume Consul master is on the same host
        self.consul_ = pyconsul.http.Consul()

    def get(self):
        ''' Inspect Hivy, docker, salt-master and consul states '''
        docker_version, docker_status = dna.utils.docker_check()

        return flask.jsonify({
            'state': {
                'hivy': os.environ.get('HIVY_STATUS', True),
                'sub-systems': {
                    'docker': docker_status,
                    'salt-master': dna.utils.is_running('salt-master'),
                    'consul': self.consul_.status
                }
            },
            'version': {
                'hivy': {
                    'major': self.hivy_version.major,
                    'minor': self.hivy_version.minor,
                    'patch': self.hivy_version.patch
                },
                'docker': docker_version,
                'consul': 'not implemented',
                'salt': saltstack.version()
            }
        })


class Doc(restful.Resource):
    ''' Expose last api documentation '''

    def get(self):
        ''' Expose doc on GET /v0/doc '''
        return flask.jsonify({
            'api': {
                'GET /': Status.__doc__,
                hivy.utils.api_doc('docs', 'GET'): Doc.__doc__,
                hivy.utils.api_doc(
                    'nodes', 'GET',
                    where='localhost'): Fleet.__doc__,
                hivy.utils.api_doc(
                    'nodes/<string:image>',
                    'GET | POST | PUT | DELETE',
                    user='dockerfile', where='localhost'): RestfulNode.__doc__,
                hivy.utils.api_doc(
                    'users/<string:username>',
                    'GET | PUT'): dna.apy.resources.User.__doc__,
                hivy.utils.api_doc(
                    'proxy/<string:frontend>',
                    'GET | POST | PUT | DELETE',
                    node='ghost', name='blog', reset=True):
                        RestfulHipache.__doc__
            }
        })
