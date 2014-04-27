# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  :copyright (c) 2014 Hive Tech, SAS.
  :license: Apache 2.0, see LICENSE for more details.
'''

import yaml
import dna.utils
from hivy import __version__


def api_url(resource):
    ''' Harmonize api endpoints '''
    return '/v{}/{}'.format(dna.utils.Version(__version__).major, resource)


def api_doc(resource, method='GET', **kwargs):
    ''' Wrap api endpoints with more details '''
    doc = '{} {}'.format(method, api_url(resource))
    params = '&'.join(['{}={}'.format(k, v) for k, v in kwargs.iteritems()])
    if params:
        doc = '?'.join([doc, params])
    return doc


def write_yaml_data(filepath, data):
    ''' Dump a dictionnary into a file as yaml '''
    with open(filepath, 'w') as yaml_fd:
        yaml_fd.write(yaml.dump(data))


# NOTE Make it a generic method ?
def clean_request_data(request_data):
    ''' Make sure data dict is utf-8 encoded '''
    data = {}
    genes = map(lambda x: x.encode('utf-8'), request_data.pop('gene'))

    data = {key.encode('utf-8'):
            map(lambda x: x.encode('utf-8'), value)
            if isinstance(value, list) else value.encode('utf-8')
            for key, value in request_data.iteritems()}

    return genes, data
