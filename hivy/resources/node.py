# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  node resource
  ---------------

  Expose Hivy containers management.

  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''


#import salt.client
import os
from flask.ext import restful
import flask
import hivy.auth as auth
from hivy.node.foundation import NodeFoundation
from hivy.logger import logger

log = logger(__name__)


class RestfulNode(restful.Resource):
    ''' The "node foundation" as a restful resource '''

    method_decorators = [auth.requires_token_auth]
    default_image = os.environ.get('NODE_IMAGE', 'quay.io/hackliff/node')
    node_name_semantic = '{}-node'

    def _node_name(self):
        ''' Customize the standard node name to the user '''
        return self.node_name_semantic.format(flask.g.get('user'))

    def get(self):
        ''' Fetch and return node informations '''
        log.info('request node information', user=flask.g.get('user'))
        return NodeFoundation(self.default_image, self._node_name()).inspect()

    def post(self):
        ''' Create and register a new node '''
        log.info('request node creation', user=flask.g.get('user'))
        node = NodeFoundation(self.default_image, self._node_name())
        feedback = node.activate()
        # Wait for the node to boot
        registration, success = node.register()
        feedback.update({
            'registration': {
                'message': registration,
                'success': success
            }
        })
        return feedback

    def delete(self):
        ''' remove an existing node '''
        log.info('request node destruction', user=flask.g.get('user'))
        node = NodeFoundation(self.default_image, self._node_name())
        unregistration, success = node.forget()
        feedback = node.destroy()
        feedback.update({
            'unregistration': {
                'message': unregistration,
                'success': success
            }
        })
        return feedback
