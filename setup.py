# coding: utf-8
"""
:copyright: 2014 Bilal Syed Hussain
:license: Apache 2.0
"""

import sys
import artistTranslateVgmdb

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def readme():
    with open('Readme.rst') as f:
        return f.read()

def requirements():
    install_requires = []
    with open('requirements.txt') as f:
        for line in f:
            install_requires.append(line.strip())

    return install_requires

setup(
    name='artist-translate-vgmdb',
    version=artistTranslateVgmdb.__version__,
    description=artistTranslateVgmdb.__doc__.strip(),
    long_description=readme(),
    url='https://github.com/Bilalh/artist-translate-vgmdb',
    author=artistTranslateVgmdb.__author__,
    author_email='bilalshussain@gmail.com',
    license=artistTranslateVgmdb.__license__,
    packages=['artistTranslateVgmdb'],
    entry_points={'console_scripts': ['artist-translate-vgmdb = artistTranslateVgmdb.__main__:main']},
    install_requires=requirements(),
    classifiers=[
        "License :: OSI Approved",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Utilities",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    keywords=['iTunes', 'ratings', 'music', 'translation'],
    include_package_data=True,
    zip_safe=False,
)
