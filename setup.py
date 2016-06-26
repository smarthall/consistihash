#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    # Project Details
    name='consistihash',
    version='0.1',
    packages=['consistihash'],

    # Dependencies
    dependency_links=[
    ],

    install_requires=[
    ],

    # Scripts
    entry_points = {
        'console_scripts': [
        ],
    },

    # Metadata for PyPI
    description='Implementation of a consistent hashing algorithm for load balancing.',
    author='Daniel Hall',
    author_email='consistihash@danielhall.me',
    url='http://www.danielhall.me/',
    include_package_data=False,
)

