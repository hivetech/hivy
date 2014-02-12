# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import os
import sh
import docker
from flask.ext import restful

from hivy import __api__
import hivy.utils as utils


class Status(restful.Resource):

    def _hivy_status(self):
        return os.environ.get('HIVY_STATUS', True)

    def get(self):
        #TODO Get hivy servers, salt, docker and serf real status
        return {
            'hivy': self._hivy_status(),
            'sub-systems': {
                'docker': utils.is_running('docker'),
                'salt-master': utils.is_running('salt-master'),
                'serf': utils.is_running('serf')
            }
        }


class Version(restful.Resource):

    dock = docker.Client('unix:///var/run/docker.sock')

    def get(self):
        # TODO Get Serf, salt and docker versions as well
        version = utils.Version()
        return {
            'hivy': {
                'major': version.major,
                'minor': version.minor,
                'patch': version.patch},
            'docker': self.dock.version(),
            'serf': sh.serf('--version').split('\n')[:-1],
            'salt': sh.salt('--version').split('\n')[:-1]
        }


class Doc(restful.Resource):

    def get(self):
        return {'api': __api__}
