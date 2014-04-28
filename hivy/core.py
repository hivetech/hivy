# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import apy.core
import hivy.conf


def main():
    # Sentry setup depends on environment variable
    application = apy.core.App(hivy.conf.ROUTES)

    # Parse the command line and serve the API
    return application.serve(
        description='Hivy, Hive api {}'.format(hivy.__version__)
    )
