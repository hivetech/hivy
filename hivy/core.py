# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Hivy Flask app
  --------------

  :copyright (c) 2014 Hive Tech, SAS.
  :license: %LICENCE%, see LICENSE for more details.
'''


from flask import Flask
from flask.ext import restful
import os
import hivy.conf as conf
import hivy.logger as logger

log = logger.logger(__name__)


app = Flask(__name__)
app.config.update(
    PROPAGATE_EXCEPTIONS=False,
    PRESERVE_CONTEXT_ON_EXCEPTION=True,
    ENV=os.environ.get('APP_ENV', 'development')
)

api = restful.Api(app)
for endpoint, resource in conf.ROUTES.iteritems():
    api.add_resource(resource, endpoint)


def main(args):
    try:
        log_setup = logger.setup(level=args['--log'], show_log=args['--debug'])
        with log_setup.applicationbound():
            #TODO if utils.check_subsystems():
            log.info('server ready',
                     log=args['--log'],
                     debug=args['--debug'],
                     bind='{}:{}'.format(args['--bind'], args['--port']))

            app.run(host=args['--bind'],
                    port=int(args['--port']),
                    debug=args['--debug'])
            exit_status = 0

    except Exception as error:
        if args['--debug']:
            raise
        log.error('%s: %s', type(error).__name__, str(error))
        exit_status = 1

    finally:
        log.info('session ended with status {}'.format(exit_status))

    return exit_status
