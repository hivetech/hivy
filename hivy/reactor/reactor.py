# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import sh
import os

import hivy.utils as utils


class Serf(object):

    def __init__(self, path='/usr/local/bin/serf'):
        assert os.path.exists(path)
        self.serf = sh.Command(path)

    def _ready(self):
        return utils.is_running('serf')

    def _serf_command(self, command, ip):
        if self._ready():
            try:
                feedback = self.serf(command, ip)
                flag = True
            except Exception, error:
                feedback = error.message
                flag = False
        else:
            feedback = 'no local agent detected, abort'
            flag = False
        return str(feedback), flag

    def version(self):
        return self.serf('--version').split('\n')[:-1]

    def register_node(self, ip):
        return self._serf_command('join', ip)

    def unregister_node(self, ip):
        return self._serf_command('force-leave', ip)
