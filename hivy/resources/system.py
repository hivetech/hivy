# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import os
from flask.ext import restful
from hivy import __api__
import hivy.utils as utils


class Status(restful.Resource):

    def _hivy_status(self):
        return os.environ.get('HIVY_STATUS', 'ok')

    def get(self):
        #TODO Get hivy servers, salt, docker and serf real status
        return {
            'hivy': self._hivy_status(),
            'sub-systems': {
                'docker': 'ok',
                'salt-master': 'ok',
                'serf': 'ok'
            }
        }


class Version(restful.Resource):

    def get(self):
        # TODO Get Serf, salt and docker versions as well
        version = utils.Version()
        return {
            'hivy': {
                'major': version.major,
                'minor': version.minor,
                'patch': version.patch},
            'docker': {
                'server': '0.7.6',  # dock.version()
                'client': '0.7.6',
                'lxc': '1.0.0.alpha1',
                'go': '1.2'},
            'serf': {
                'agent': '0.4.1',
                'protocol': '3'},
            'salt': '0.17.5'
        }


class Doc(restful.Resource):

    def get(self):
        return {'api': __api__}
