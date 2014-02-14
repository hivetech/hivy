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
import sh
import docker
from flask.ext import restful

from hivy import __api__, DOCKER_ON, SALT_ON, SERF_ON
import hivy.utils as utils
import hivy.reactor.reactor as reactor


class Status(restful.Resource):
    ''' Expose Hivy services states and versions '''

    def __init__(self):
        self.hivy_version = utils.Version()
        self.serf = reactor.Serf()
        self.salt = sh.Command('/usr/bin/salt-master')
        docker_url = os.environ.get('DOCKER_URL', 'unix://var/run/docker.sock')
        self.dock = docker.Client(base_url=docker_url,
                                  version='0.7.6',
                                  timeout=10)

    def get(self):
        ''' Inspect Hivy, docker, salt-master and serf states '''

        return {
            'state': {
                'hivy': os.environ.get('HIVY_STATUS', True),
                'sub-systems': {
                    'docker': DOCKER_ON,
                    'salt-master': SALT_ON,
                    'serf': SERF_ON
                }
            },
            'version': {
                'hivy': {
                    'major': self.hivy_version.major,
                    'minor': self.hivy_version.minor,
                    'patch': self.hivy_version.patch
                },
                'docker': self.dock.version(),
                'serf': self.serf.version(),
                'salt': str(self.salt('--version'))
            }
        }


class Doc(restful.Resource):
    ''' Expose last api documentation '''

    def get(self):
        ''' No magic here, see hivy.__setup__.py '''
        return {'api': __api__}
