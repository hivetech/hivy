web: ./app/hivy --bind 0.0.0.0 --debug
Sneezy: celery worker -A telepathy.trades -n sneezy.%h --loglevel info
Grumpy: celery worker -A telepathy.trades -n grumpy.%h --loglevel info
