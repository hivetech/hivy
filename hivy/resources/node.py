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


class RestNode(restful.Resource):

    method_decorators = [auth.requires_token_auth]
    default_image = os.environ.get('NODE_IMAGE', 'quay.io/hackliff/node')

    def _node_name(self):
        return '{}-lab'.format(flask.g.get('user'))

    def get(self):
        return NodeFoundation(self.default_image, self._node_name()).inspect()

    def post(self):
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
