import os
from setuptools import setup, find_packages

from hivy import __project__, __version__, __author__, __licence__


# Needs also : apt-get install swig
requires = [
    'Flask-RESTful>=0.2.11',
    'docopt>=0.6.1',
    'itsdangerous>=0.23',
    'pytz>=2013.9',
    'salt>=0.17.5',
    'nose>=1.3.0',
    'Flask-Testing',
    'docker-py>=0.2.3']


def long_description():
    try:
        #with codecs.open(readme, encoding='utf8') as f:
        with open('readme.md') as f:
            return f.read()
    except IOError:
        return "failed to read README.md"


setup(
    name=__project__,
    version=__version__,
    description='This plugin provides a RESTFul interface to unide',
    author=__author__,
    author_email='xavier.bruhiere@gmail.com',
    packages=find_packages(),
    long_description=long_description(),
    license=__licence__,
    install_requires=requires,
    url="https://github.com/hivetech/hivy",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development',
        'Topic :: System :: Shells',
    ],
    scripts=['app/hivy'],
    data_files=[(os.path.expanduser('~/.hivy'), ['app/Procfile'])]
)
