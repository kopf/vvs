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
          author='Aengus Walton',
          author_email='ventolin@gmail.com',
          url='https://github.com/kopf/vvs',
          packages=find_packages(exclude=['tests', 'test']),
          classifiers=[
              'Development Status :: 4 - Beta',
              'Programming Language :: Python',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5'
          ],
          zip_safe=False,
          include_package_data=True,
          setup_requires=['setuptools_scm'],
          install_requires=['beautifulsoup4==4.5.1', 'click==6.6', 'requests==2.11.1'],
          use_scm_version=True,
          entry_points=ENTRY_POINTS)


if __name__ == "__main__":
    setup_package()