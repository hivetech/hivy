# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Hivy
  ----

  Hivy exposes a RESTful API to the Unide (unide.co) platform. Create, destroy
  and configure collaborative development environments and services around it.

  :copyright (c) 2014 Xavier Bruhier.
  :license: Apache 2.0, see LICENSE for more details.
'''


__project__ = 'hivy'
__author__ = 'Xavier Bruhiere'
__copyright__ = 'Hive Tech, SAS'
__licence__ = 'Apache 2.0'
__version__ = '0.0.5'
__api__ = {
    'status': 'GET /',
    'doc': 'GET /doc',
    'node': 'GET | POST | DELETE /node'
}
