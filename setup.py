#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from setuptools import setup, find_packages


ENTRY_POINTS = """
    [console_scripts]
    vvs=vvs.cli:main
"""


def setup_package():
    setup(name='vvs',
          description='Displays upcoming departure times from stations on the Stuttgart public transport network',
          long_description=open('README.rst').read(),
          author='Aengus Walton',
          author_email='ventolin@gmail.com',
          url='https://github.com/kopf/vvs',
          license='Apache',
          packages=find_packages(exclude=['tests', 'test']),
          classifiers=[
              'Development Status :: 4 - Beta',
              'License :: OSI Approved :: Apache Software License',
              'Programming Language :: Python',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5'
          ],
          zip_safe=False,
          include_package_data=True,
          setup_requires=['setuptools_scm'],
          install_requires=['beautifulsoup4', 'click', 'requests', 'pytz'],
          use_scm_version=True,
          entry_points=ENTRY_POINTS)


if __name__ == "__main__":
    setup_package()