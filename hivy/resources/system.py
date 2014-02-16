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
#import sh
from flask.ext import restful
from hivy import __api__
import hivy.utils as utils
import hivy.reactor.reactor as reactor
from hivy.logger import logger

log = logger(__name__)


class Status(restful.Resource):
    ''' Expose Hivy services states and versions '''

    def __init__(self):
        self.hivy_version = utils.Version()
        self.serf = reactor.Serf()
        #self.salt = sh.Command('/usr/bin/salt-master')

    def get(self):
        ''' Inspect Hivy, docker, salt-master and serf states '''
        log.info('request hivy status')
        docker_version, docker_status = utils.docker_check()

        return {
            'state': {
                'hivy': os.environ.get('HIVY_STATUS', True),
                'sub-systems': {
                    'docker': docker_status,
                    'salt-master': 'not implemented',
                    'serf': utils.is_available('serf')
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
                'salt': 'not implemented'
            }
        }


class Doc(restful.Resource):
    ''' Expose last api documentation '''

    def get(self):
        ''' No magic here, see hivy.__setup__.py '''
        log.info('request hivy doc')
        return {'api': __api__}
