# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  node resource
  -------------

  Expose Hivy containers management.

  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''


import time
import flask
from flask.ext import restful
from flask.ext.restful import reqparse
import hivy.auth as auth
from hivy.node.foundation import NodeFoundation
import dna.logging

log = dna.logging.logger(__name__)


class RestfulNode(restful.Resource):
    ''' The "node foundation" as a restful resource '''

    method_decorators = [auth.requires_token_auth]
    #default_image = os.environ.get('NODE_IMAGE', 'quay.io/hackliff/node')
    node_name_semantic = '{}-{}'
    image_name_semantic = '{}/{}/{}:{}'

    def _node_name(self, image):
        ''' Customize the standard node name to the user '''
        return self.node_name_semantic.format(
            flask.g.get('user'), image)

    def _image_name(self, image):
        ''' Customize the standard node name to the user '''
        tag = 'latest'
        provider = 'quay.io'
        return self.image_name_semantic.format(
            provider, flask.g.get('user'), image, tag)

    def get(self, image):
        ''' Fetch and return node informations '''
        log.info('request node information', user=flask.g.get('user'))
        return NodeFoundation(
            self._image_name(image), self._node_name(image)).inspect()

    def post(self, image):
        ''' Create and register a new node '''
        log.info('request node creation', user=flask.g.get('user'))
        node = NodeFoundation(self._image_name(image), self._node_name(image))
        feedback = node.activate()
        # Wait for the node to boot
        # TODO Replace below by node.wait_boot()
        time.sleep(10)
        registration, success = node.register()
        feedback.update({
            'registration': {
                'message': registration,
                'success': success
            }
        })
        return feedback

    def delete(self, image):
        ''' remove an existing node '''
        log.info('request node destruction', user=flask.g.get('user'))
        node = NodeFoundation(self._image_name(image), self._node_name(image))
        unregistration, success = node.forget()
        feedback = node.destroy()
        feedback.update({
            'unregistration': {
                'message': unregistration,
                'success': success
            }
        })
        return feedback

    def put(self, image):
        ''' Manipulate the given node '''
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str)
        args = parser.parse_args()

        node = NodeFoundation(self._image_name(image), self._node_name(image))
        result = node.synthetize(flask.g.get('user'), args.get('gene', ''), {})
        return result
