# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''

import flask
from flask.ext.restful import reqparse
import dna.logging
from dna.apy.resources import SecuredRestfulResource
import hivy.proxy

log = dna.logging.logger(__name__)


# TODO Fetch ip and port from image names
class RestfulHipache(SecuredRestfulResource):
    ''' Hipache High level management '''

    # Connection uses environment variables
    _hipache = hivy.proxy.Hipache()

    def get(self, frontend):
        ''' Fetch current proxy mapping '''
        if frontend == 'all':
            mapping = self._hipache.mapping
        elif frontend in self._hipache.mapping:
            mapping = self._hipache.mapping[frontend]
        else:
            flask.abort(404)
        log.info('inspect proxy', mapping=mapping)
        return mapping

    def post(self, frontend):
        ''' Map a node to the given frontend '''
        parser = reqparse.RequestParser()
        parser.add_argument('node', type=str, action='append')
        # NOTE <name> parameter is pretty useless
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('reset', type=bool, default=False)
        args = parser.parse_args()

        self._hipache.check_and_register_frontend(
            frontend, args['name'], args['reset']
        )
        if args.get('node'):
            self._hipache.map_backends(frontend, args['node'])

        return self._hipache.mapping

    def put(self, frontend):
        ''' Update an exisiting frontend mapping '''
        parser = reqparse.RequestParser()
        parser.add_argument('node', type=str, action='append', required=True)
        parser.add_argument('name', type=str)
        args = parser.parse_args()

        if args.get('name'):
            self._hipache.check_and_register_frontend(
                frontend, args['name'], replace=True
            )

        self._hipache.map_backends(frontend, args['node'])

        return self._hipache.mapping

    def delete(self, frontend):
        ''' Remove from hipache the given frontend '''
        success = self._hipache.reset() if frontend == 'all' \
            else self._hipache.remove_frontend(frontend)
        return {'removed': success}
