#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from mootdx import __version__

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pytdx', 'click',]
test_requirements = ['pytdx', 'click', 'pytest',]
setup_requirements = ['pytdx', 'click', 'pytest-runner',]

setup(
    name='mootdx',
    version=__version__,
    description="tdx reader",
    long_description=readme + '\n\n' + history,
    author="bopo.wang",
    author_email='ibopo@126.com',
    url='https://github.com/bopo/mootdx',
    packages=find_packages(include=['mootdx','mootdx.*']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mootdx',
    entry_points={
        'console_scripts': [
            'mootdx = mootdx.cli:main',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
