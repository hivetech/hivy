Hivy
====

> Unide Hive controller

Installation
------------

Docker must be [installed](http://www.docker.io/gettingstarted/) on the server
your are deploying the environments.

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
$ hivy --bind 0.0.0.0 --debug
```

And play with it in another terminal

```console
curl -H "Authorization:<ACCESS_TOKEN>" http://0.0.0.0:5000/

# Create a new environment
curl -X POST -H "Authorization:<ACCESS_TOKEN>" http://0.0.0.0:5000/node

# Destroy it
curl -X DELETE -H "Authorization:<ACCESS_TOKEN>" http://0.0.0.0:5000/node
```
