import sys
import os
from setuptools import setup, find_packages
from hivy import __project__, __version__, __author__, __licence__


if sys.argv[-1] == 'test':
    status = os.system('make tests')
    sys.exit(1 if status > 127 else status)


# Needs also : apt-get install swig
requires = [
    'pyzmq>=14.2.0',
    'pyconsul>=0.0.2',
    'dna>=0.0.4',
    'redis>=2.9.1',
    'Flask-RESTful>=0.2.11',
    'docopt>=0.6.1',
    'itsdangerous>=0.23',
    'pytz>=2013.9',
    'salt>=2014.1.3',
    'blinker>=1.3',
    'sh>=1.09',
    'docker-py>=0.3.1'
]


def long_description():
    try:
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
    entry_points={
        'console_scripts': [
            'hivy = hivy.__main__:main',
        ],
    },
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
    data_files=[(os.path.expanduser('~/.hivy'), ['./Procfile'])]
)
