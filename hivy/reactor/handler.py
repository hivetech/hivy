# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Garethr


import os


class SerfHandler(object):

    def __init__(self):
        #TODO Payload on stdin
        #TODO All SERF_TAG_* variables
        #NOTE .get() are for testing, remove it later ?
        self.name = os.environ.get('SERF_SELF_NAME')
        self.role = os.environ.get('SERF_SELF_ROLE')
        if os.environ.get('SERF_EVENT', '') == 'user':
            self.event = os.environ.get('SERF_USER_EVENT')
        else:
            self.event = os.environ.get('SERF_EVENT', '').replace('-', '_')

    def log(self, message):
        print(message)
        with open('/tmp/hook.log', 'a') as fd:
            fd.write(message + '\n')


class SerfHandlerProxy(SerfHandler):

    def __init__(self):
        super(SerfHandlerProxy, self).__init__()
        self.handlers = {}

    def register(self, role, handler):
        self.handlers[role] = handler

    def get_klass(self):
        klass = False
        if self.role in self.handlers:
            klass = self.handlers[self.role]
        elif 'default' in self.handlers:
            klass = self.handlers['default']
        return klass

    def run(self):
        klass = self.get_klass()
        if not klass:
            self.log("no handler for role")
        else:
            try:
                getattr(klass, self.event)()
            except AttributeError:
                self.log("event not implemented by class")
