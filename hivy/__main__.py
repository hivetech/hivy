#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Hivy Flask app
  --------------

  :copyright (c) 2014 Hive Tech, SAS.
  :license: %LICENCE%, see LICENSE for more details.
'''

import sys
import dna.apy.core
import hivy.conf


def main():
    # Sentry and Database setup depends on environment variable
    #     - SENTRY_DNS [None]
    #     - MONGODB_NAME [apy]
    #     - MONGODB_HOST [localhost]
    #     - MONGODB_PORT [27017]
    application_ = dna.apy.core.Application
    application_.setup_db()
    application_.setup_routes(hivy.conf.ROUTES)

    # Parse the command line and serve the API
    return application_.serve(
        description='Hivy, Hive api {}'.format(hivy.__version__)
    )


if __name__ == '__main__':
    sys.exit(main())
