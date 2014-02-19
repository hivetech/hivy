# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''Hivy

Usage:
  hivy -h | --help
  hivy --version
  hivy [--bind=<ip>] [--port=<port>] [-d | --debug] [--log <level>]

Options:
  -h --help       Show this screen.
  --version       Show version.
  --debug         Activates Flask debug
  --bind=<ip>     Listens on the given ip [default: 127.0.0.1]
  --port=<port>   Listens on the given port [default: 5000]
  --log=<level>   Log output level [default: debug]
'''


from flask import Flask
from flask.ext import restful
import os
from docopt import docopt
from hivy import __version__
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


def main():
    args = docopt(__doc__, version='Hivy, Hive api {}'.format(__version__))
    exit_status = 0
    log_setup = logger.setup(level=args['--log'], show_log=args['--debug'])
    with log_setup.applicationbound():
        try:
            #TODO if utils.check_subsystems():
            log.info('server ready',
                     log=args['--log'],
                     debug=args['--debug'],
                     bind='{}:{}'.format(args['--bind'], args['--port']))

            app.run(host=args['--bind'],
                    port=int(args['--port']),
                    debug=args['--debug'])

        except Exception as error:
            if args['--debug']:
                raise
            log.error('{}: {}'.format(type(error).__name__, str(error)))
            exit_status = 1

        finally:
            log.info('session ended with status {}'.format(exit_status))

    return exit_status
