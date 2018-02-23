# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup

VERSION = (1, 0, 8)

__version__ = ".".join(str(i) for i in VERSION)

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="treebo-csv-uploader",
    version=__version__,
    author="Utkarsh Mishra",
    author_email="utkarsh.mishra@treebohotels.com",
    description=("Generic csv upload with pluggable actions"),
    license="BSD",
    keywords="csv upload",
    url="https://github.com/TreeboHotels/treebo_csv_uploader",
    packages=find_packages(exclude=['tests', 'docs']),
    package_data={'templates': ['templates/csv_uploader.html']},
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: System :: Logging',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities',
    ],
    install_requires=['django'],
    include_package_data=True,
    zip_safe=False,
)
