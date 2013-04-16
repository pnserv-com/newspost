# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

version = '0.0.0'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'nckvs-client'
]

tests_require = requires + [
    'pytest',
    'mock'
]

dependency_links = [
    'https://github.com/tin-com/nckvs-client/tarball/develop#egg=nckvs-client-0.0.0dev',
]

setup(name='newspost',
      version=version,
      description='A simple data posting program for json news',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP"
      ],
      author='Yoshihisa Tanaka',
      author_email='yoshihisa@iij.ad.jp',
      url='https://github.com/tin-com/newspost',
      keywords='web',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      dependency_links=dependency_links,
      install_requires=requires,
      tests_require=tests_require)
