# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import os
import re

from setuptools import setup, find_packages

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.join(ROOT_PATH, 'source')
README_PATH = os.path.join(ROOT_PATH, 'README.rst')

PACKAGE_NAME = 'clique'

# Read version from source.
with open(
    os.path.join(SOURCE_PATH, PACKAGE_NAME, '_version.py')
) as _version_file:
    VERSION = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)


# Compute dependencies.
SETUP_REQUIRES = [
    'sphinx >= 1.2.2, < 2',
    'sphinx_rtd_theme >= 0.1.6, < 1',
    'pytest-runner >= 2.7, < 3'
]
INSTALL_REQUIRES = [
]
TEST_REQUIRES = [
    'pytest >= 2.3.5, < 3',
    'pytest-cov >= 2, < 3'
]

# Readthedocs requires Sphinx extensions to be specified as part of
# install_requires in order to build properly.
if os.environ.get('READTHEDOCS', None) == 'True':
    INSTALL_REQUIRES.extend(SETUP_REQUIRES)


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description='Manage collections with common numerical component',
    long_description=open(README_PATH).read(),
    keywords='sequence, pattern, filesystem, collection, numerical',
    url='https://gitlab.com/4degrees/clique',
    author='Martin Pengelly-Phillips',
    author_email='martin@4degrees.ltd.uk',
    license='Apache License (2.0)',
    packages=find_packages(SOURCE_PATH),
    package_dir={
        '': 'source'
    },
    setup_requires=SETUP_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES,
    extras_require={
        'setup': SETUP_REQUIRES,
        'tests': TEST_REQUIRES,
        'dev': SETUP_REQUIRES + TEST_REQUIRES
    },
    zip_safe=False
)
