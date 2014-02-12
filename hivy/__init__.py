'''
TODO: Doc
'''


__project__ = 'hivy'
__author__ = 'Xavier Bruhiere'
__copyright__ = 'Hive Tech, SAS'
__licence__ = 'Apache 2.0'
__version__ = '0.0.4'
__api__ = {
    'status': 'GET /status',
    'version': 'GET /version',
    'doc': 'GET /doc',
    'node': 'GET | POST | DELETE /node'
}


from flask import Flask, request
from flask.ext import restful
import os

import hivy.settings as settings


app = Flask(__name__)
app.config.update(
    PROPAGATE_EXCEPTIONS=False,
    PRESERVE_CONTEXT_ON_EXCEPTION=True,
    ENV=os.environ.get('APP_ENV', 'development')
)

api = restful.Api(app)
for endpoint, resource in settings.routes.iteritems():
    api.add_resource(resource, endpoint)


#TODO Use it for logging and perfs
@app.before_request
def before_request():
    print request


@app.after_request
def after_request(response):
    print response
    return response
