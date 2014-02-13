# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


from hivy.reactor.handler import SerfHandler


class Debug(SerfHandler):
    ''' Debug and show what's available with hooks framework '''
    def _dump_context(self):
        msg = '{} (role "{}") received an event "{}"'
        self.log(msg.format(self.name, self.role, self.event))

    def deploy(self):
        self._dump_context()

    def member_join(self):
        self._dump_context()

    def member_leave(self):
        self._dump_context()

    def member_failed(self):
        self._dump_context()

    def member_update(self):
        self._dump_context()
