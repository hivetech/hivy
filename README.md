Hivy
====

[![Latest Version](https://pypip.in/v/hivy/badge.png)](https://pypi.python.org/pypi/hivy/)
[![Build Status](https://drone.io/github.com/hivetech/hivy/status.png)](https://drone.io/github.com/hivetech/hivy/latest)
[![Coverage Status](https://coveralls.io/repos/hivetech/hivy/badge.png)](https://coveralls.io/r/hivetech/hivy)
[![Code Health](https://landscape.io/github/hivetech/hivy/master/landscape.png)](https://landscape.io/github/hivetech/hivy/master)
[![Requirements Status](https://requires.io/github/hivetech/hivy/requirements.png?branch=master)](https://requires.io/github/hivetech/hivy/requirements/?branch=master)
[![License](https://pypip.in/license/hivy/badge.png)](https://pypi.python.org/pypi/hivy/)

> Unide Hive controller

Hivy exposes a RESTful API to the [unide](unide.co) platform. Create, destroy
and configure collaborative development environments and services around it.

Installation
------------

Docker must be [installed](http://www.docker.io/gettingstarted/) on the server
your are deploying the environments.

You also need [serf v0.4.1](serfdom.io) for service orchestration.

```console
$ (sudo) pip install hivy

$ # Default settings use local docker server (using default unix sockets)
$ # But you can tell hivy to use another one
$ export DOCKER_URL="http://172.0.1.17:1234"
$ # In the same manner, you can use a custom image
$ export NODE_IMAGE=my/image
```

Usage
-----

In a first terminal, fire up the server

```console
$ serf agent -node hivy -tag role=master &
$ hivy --bind 0.0.0.0 --debug
```

And play with it in another terminal

```console
curl -H "Authorization:<ACCESS_TOKEN>" http://0.0.0.0:5000/

# Get some informations
curl http://0.0.0.0:5000/
curl http://0.0.0.0:5000/version
curl http://0.0.0.0:5000/v0/doc

# Create a new environment
curl -X POST -H "Authorization:<ACCESS_TOKEN>" http://0.0.0.0:5000/v0/node

# Destroy it
curl -X DELETE -H "Authorization:<ACCESS_TOKEN>" http://0.0.0.0:5000/v0/node
```

Tests
-----

```console
$ Make tests

$ # If docker is installed, you can test node interactions as well
$ USE_DOCKER=true make tests
```
