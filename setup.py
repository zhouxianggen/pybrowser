#!/usr/bin/env python
#coding=utf8

try:
    from  setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
        name = 'pybrowser',
        version = '1.0',
        install_requires = ['pyppeteer', 'psutil'], 
        description = 'python browser',
        url = 'https://github.com/zhouxianggen/pybrowser', 
        author = 'zhouxianggen',
        author_email = 'zhouxianggen@gmail.com',
        classifiers = [ 'Programming Language :: Python :: 3.7',],
        packages = ['pybrowser'],
        data_files = [ ], 
        )

