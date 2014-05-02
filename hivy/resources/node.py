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
import flask
import dna.logging
from dna.apy.resources import SecuredRestfulResource
import hivy.utils as utils
import hivy.settings as settings
from hivy.node.foundation import NodeFoundation

log = dna.logging.logger(__name__)


class Fleet(SecuredRestfulResource):
    ''' User nodes organization '''

    def __init__(self):
        docker_url = os.environ.get('DOCKER_URL', settings.DEFAULT_DOCKER_URL)
        self.dock = docker.Client(
            base_url=docker_url, version='0.7.6', timeout=10
        )

    def get(self):
        ''' Provide nodes fleet overview '''
        # TODO Limited to user nodes
        report = {}
        for node in self.dock.containers():
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


# TODO Support custom provider
class RestfulNode(SecuredRestfulResource):
    ''' The "node foundation" as a restful resource '''

    default_user = 'johndoe'
    node_name_semantic = '{}-{}'
    image_name_semantic = '{}/{}:{}'

    @property
    def user(self):
        user_ = flask.g.get('user')
        return user_.username if user_ else self.default_user

    def _node_name(self, image):
        ''' Customize the standard node name to the user '''
        return self.node_name_semantic.format(self.user, image)

    def _image_name(self, image):
        ''' Customize the standard node name to the user '''
        tag = 'latest'
        return self.image_name_semantic.format(
            self.user, image, tag)

    def get(self, image):
        ''' Fetch and return node informations '''
        log.info('request node information', user=self.user)
        return NodeFoundation(
            self._image_name(image), self._node_name(image)).properties

    def post(self, image):
        ''' Create and register a new node '''
        data = flask.request.get_json() if flask.request.json else {}
        log.info('request node creation', user=self.user, data=data)

        node = NodeFoundation(self._image_name(image), self._node_name(image))

        for link in data.get('links', []):
            log.info('acquiring new link', link=link)
            node.discover(link)

        return node.activate(data.get('ports', []), data.get('env', {}))

    def delete(self, image):
        ''' remove an existing node '''
        log.info('request node destruction', user=self.user)
        node = NodeFoundation(self._image_name(image), self._node_name(image))
        feedback = node.destroy()
        is_success = node.forget()
        feedback.update({'unregistration': is_success})
        return feedback

    def put(self, image):
        ''' Manipulate the given node '''
        node = NodeFoundation(self._image_name(image), self._node_name(image))
        results = {}
        if not flask.request.json or 'gene' not in flask.request.json:
            flask.abort(400)

        data = utils.to_utf8_dict(flask.request.get_json())
        genes = data.pop('gene', [])
        for gene in genes:
            results[gene] = node.synthetize(self.user, gene, data)
        return results
