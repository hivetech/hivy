# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Util hooks
  ----------

  Some generic handlers

  :copyright (c) 2014 Xavier Bruhier.
  :license: Apache 2.0, see LICENSE for more details.
'''


from hivy.reactor.handler import SerfHandler


class Debug(SerfHandler):
    '''
    Debug and show what's available with hooks framework
    http://www.serfdom.io/intro/getting-started/event-handlers.html
    '''

    def _dump_context(self):
        ''' Human-friendly serf environment informations in a file '''
        msg = '{} (role "{}") received an event "{}"'
        self.log(msg.format(self.name, self.role, self.event))

    def deploy(self):
        ''' Custom user event '''
        self._dump_context()

    def member_join(self):
        ''' Triggered when a new agent joined the cluster '''
        self._dump_context()

    def member_leave(self):
        ''' Triggered when an agent gracefully left the cluster '''
        self._dump_context()

    def member_failed(self):
        ''' Triggered when an agent disappeared from the cluster '''
        self._dump_context()

    def member_update(self):
        ''' Triggered when an agent updates its informations '''
        self._dump_context()
