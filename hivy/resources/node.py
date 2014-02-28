# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  node resource
  -------------

  Expose Hivy containers management.

  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''


import os
import docker
import time
import flask
from flask.ext import restful
from flask.ext.restful import reqparse
import hivy.auth as auth
import hivy.utils as utils
from hivy.node.foundation import NodeFoundation
import dna.logging

log = dna.logging.logger(__name__)


class Fleet(restful.Resource):
    ''' User nodes organization as a restful resource '''

    method_decorators = [auth.requires_token_auth]

    def __init__(self):
        docker_url = os.environ.get('DOCKER_URL', 'unix://var/run/docker.sock')
        self.dock = docker.Client(
            base_url=docker_url, version='0.7.6', timeout=10)

    def get(self):
        ''' Provide nodes fleet overview '''
        # TODO Limited to user nodes
        report = {}
        nodes = self.dock.containers()
        for node in nodes:
            report[node['Names'][0]] = {
                'created': node['Created'],
                'image': node['Image'],
                'status': node['Status'],
                'network': {}
            }
            for port in node['Ports']:
                report[node['Names'][0]]['network'][port['PublicPort']] = \
                    '{}://{}:{}'.format(
                        port['Type'], port['IP'], port['PrivatePort'])
        return report


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
        parser = reqparse.RequestParser()
        parser.add_argument('link', type=str, action='append')
        parser.add_argument('port', type=int, action='append')
        args = parser.parse_args()

        log.info('request node creation', user=flask.g.get('user'))
        node = NodeFoundation(self._image_name(image), self._node_name(image))

        for link in args['link']:
            log.info('acquiring new link', link=link)
            node.discover(link)

        feedback = node.activate(args['port'])
        # Wait for the node to boot
        # TODO Replace below by node.wait_boot()
        if not 'error' in feedback:
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
        node = NodeFoundation(self._image_name(image), self._node_name(image))
        results = {}
        if not flask.request.json or not 'gene' in flask.request.json:
            flask.abort(400)

        genes, data = utils.clean_request_data(flask.request.get_json())
        for gene in genes:
            results[gene] = node.synthetize(flask.g.get('user'), gene, data)
        return results
