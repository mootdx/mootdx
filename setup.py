#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import find_packages, setup


def parse_requirements(filename):
    line_iter = (line.strip() for line in open(filename))
    return [line for line in line_iter if line and not line.startswith("#")]


with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', encoding='utf-8') as history_file:
    history = history_file.read()

requirements = parse_requirements('requirements.txt')
test_requirements = requirements
test_requirements.append('pytest')

setup(
    name='mootdx',
    version='0.7.11',
    description="通达信数据读取接口.",
    long_description=readme,
    author="bopo.wang",
    author_email='ibopo@126.com',
    url='https://github.com/bopo/mootdx',
    packages=find_packages(include=['mootdx', 'mootdx.*']),
    # include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mootdx',
    entry_points={'console_scripts': [
        'mootdx=mootdx.__main__:entry',
    ]},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=requirements,
)
