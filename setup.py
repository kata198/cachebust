#!/usr/bin/env python
#
# Copyright (c) 2015 Timothy Savannah under terms of LGPLv2. You should have received a copy of this with this distribution as "LICENSE"


#vim: set ts=4 sw=4 expandtab

import os
import sys
from setuptools import setup


if __name__ == '__main__':
 

    dirName = os.path.dirname(__file__)
    if dirName and os.getcwd() != dirName:
        os.chdir(dirName)

    summary = 'Provide a server-side means to ensure that clients always fetch assets when they are updated'

    try:
        with open('README.rst', 'r') as f:
            long_description = f.read()
    except Exception as e:
        sys.stderr.write('Exception when reading long description: %s\n' %(str(e),))
        long_description = summary

    setup(name='cachebust',
            version='1.0.1',
            packages=['cachebust'],
            scripts=['bin/cacheBust'],
            author='Tim Savannah',
            author_email='kata198@gmail.com',
            maintainer='Tim Savannah',
            requires=['AdvancedHTMLParser', 'ArgumentParser'],
            install_requires=['AdvancedHTMLParser', 'ArgumentParser'],
            url='https://github.com/kata198/AdvancedHTMLParser',
            maintainer_email='kata198@gmail.com',
            description=summary,
            long_description=long_description,
            license='LGPLv2',
            keywords=['cache', 'bust', 'url', 'md5', 'javascript', 'css', 'asset', 'update'],
            classifiers=['Development Status :: 5 - Production/Stable',
                         'Programming Language :: Python',
                         'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
                         'Programming Language :: Python :: 2',
                          'Programming Language :: Python :: 2',
                          'Programming Language :: Python :: 2.7',
                          'Programming Language :: Python :: 3',
                          'Programming Language :: Python :: 3.3',
                          'Programming Language :: Python :: 3.4',
                          'Topic :: Internet :: WWW/HTTP',
                          'Topic :: Text Processing :: Markup :: HTML',
                          'Topic :: Software Development :: Libraries :: Python Modules',
            ]
    )



