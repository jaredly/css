#!/usr/bin/env python

from distutils.core import setup
import os

from disttest import test

setup(
    name='css',
    author='Jared Forsyth',
    author_email='jared@jaredforsyth.com',
    version='0.1',
    url='http://jaredforsyth.com/projects/css',
    download_url='http://github.com/jabapyth/css',
    packages=['css'],
    description='a small, fast css parser for python the utilizes the codetalker library',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
    cmdclass={'test': test},
    options={
        'test': {
            'test_dir': ['tests'],
        },
    },
)



# vim: et sw=4 sts=4
