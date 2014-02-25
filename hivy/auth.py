# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Hivy Authentification
  ---------------------

  Methods for protecting hivy resources

  :copyright (c) 2014 Hive Tech, SAS.
  :license: %LICENCE%, see LICENSE for more details.
'''


from functools import wraps
from flask import request, Response, g
import dna.logging


log = dna.logging.logger(__name__)


TMP_USERS = {
    'd2a879423e53ddbb6788bbc286647a793440f3db': 'hackliff',
    'd5b4596e477eab637a5b5177333ba17440287bb5': 'gekko',
    '22d047ebaedc0149ea6f1737d4a0ecac513451cf': 'johny'}


def check_credentials(username, password):
    ''' Verify basic http authentification '''
    return True


def check_token(token):
    ''' Verify http header token authentification '''
    return token in TMP_USERS


def auth_failed():
    ''' Sends a 401 response that enables basic auth '''
    return Response(
        '{"error": "Could not verify your access level for that URL. '
        'You have to login with proper credentials"}', 401,
        {'WWW-Authenticate': 'Token realm="Login Required"'})


def requires_basic_auth(resource):
    '''
    Flask decorator protecting ressources using username/password scheme
    '''
    @wraps(resource)
    def decorated(*args, **kwargs):
        ''' Check provided username/password '''
        auth = request.authorization
        # auth = {'username': 'admin', 'password': 'secret'}
        if not auth or not check_credentials(auth.username, auth.password):
            log.warn('authentification failed', credentials=auth)
            return auth_failed()
        log.info('authentification succeeded', credentials=auth)
        return resource(*args, **kwargs)
    return decorated


def requires_token_auth(resource):
    '''
    Flask decorator protecting ressources using token scheme
    '''
    @wraps(resource)
    def decorated(*args, **kwargs):
        ''' Check provided token '''
        token = request.headers.get('Authorization')
        if not token or not check_token(token):
            log.warn('authentification failed', token=token)
            return auth_failed()
        g.user = TMP_USERS[token]
        log.info('authentification succeeded', token=token, user=g.user)
        return resource(*args, **kwargs)
    return decorated
