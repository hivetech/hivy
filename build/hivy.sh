#!/bin/bash
set -e
source /build/buildconfig
set -x

$minimal_apt_get_install swig libssl-dev libzmq-dev
cd /hivy && python setup.py install
