# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  reactor subsystem
  -----------------

  Event-based, Hivy orchestrator

  :copyright (c) 2014 Garethr
  :license: Apache 2.0, see LICENSE for more details.
'''


import os
from hivy.logger import logger


log = logger('hivy.reactor.' + __name__)


class SerfHandler(object):
    ''' Wrap a serf event into a python friendly context '''

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

    def log(self, msg):
        log.info(msg, name=self.name, event_type=self.event, role=self.role)


class SerfHandlerProxy(SerfHandler):
    ''' Provide the interface between user handlers and serf events '''

    def __init__(self):
        super(SerfHandlerProxy, self).__init__()
        self.handlers = {}

    def register(self, role, handler):
        ''' Map event type with Handlers '''
        self.log('mapping handler {} with role {}'.format(handler, role))
        self.handlers[role] = handler

    def get_klass(self):
        '''
        When an event occurs, searchs for the associated handler or falls back
        to a default one if it exists
        '''
        klass = False
        if self.role in self.handlers:
            klass = self.handlers[self.role]
        elif 'default' in self.handlers:
            klass = self.handlers['default']
        return klass

    def run(self):
        '''
        If an handler is found registered with the event role, run the class
        method mapped with the event type
        '''
        self.log('received event')
        klass = self.get_klass()
        if not klass:
            self.log("no handler found")
        else:
            try:
                getattr(klass, self.event)()
            except AttributeError:
                self.log("event not implemented by class")
