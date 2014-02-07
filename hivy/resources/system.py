# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


from flask.ext import restful
from hivy import __version__, __doc__


class Status(restful.Resource):

    def get(self):
        return {'status': 'ok'}


class Version(restful.Resource):

    def get(self):
        return {'version': __version__}


class Doc(restful.Resource):

    def get(self):
        return {'doc': __doc__}
