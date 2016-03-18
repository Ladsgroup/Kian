# -*- coding: utf-8  -*-
"""Installer script for Kian."""
#
# (C) Amir Sarabadani
#
# Distributed under the terms of the MIT license.
#
import os

from setuptools import find_packages, setup


def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]


setup(
    name='kian',
    version='0.2.0',
    description='Kian is the neural network designed to serve Wikidata.',
    long_description=open('README.rst').read(),
    maintainer='Amir Sarabadani',
    maintainer_email='ladsgroup@gmail.com',
    license='MIT License',
    install_requires=requirements("requirements.txt"),
    packages=find_packages(),
    url='https://github.com/Ladsgroup/Kian',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
)
