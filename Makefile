# Makefile
# vim:ft=make

all:
	python setup.py install

package:
	python setup.py sdist
	python setup.py sdist upload

tests:
	flake8 tests hivy
	nosetests -w tests --with-coverage --cover-package=hivy
