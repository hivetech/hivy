#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


from hivy import __version__


class Version:
    ''' Provide a convenient way to manipulate version '''
    def __init__(self):
        _version = __version__.split('.')
        self.major = int(_version[0])
        self.minor = int(_version[1])
        self.patch = int(_version[2])


def api_url(resource):
    return '/v{}/{}'.format(Version().major, resource)
