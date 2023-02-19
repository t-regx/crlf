#!/usr/bin/env python3
from setuptools import setup, find_packages

from crlf import __version__
from version import get_and_increment

setup(name='crlf',
      python_requires='~=3.6',
      version=f'{__version__}.dev{get_and_increment()}',
      packages=find_packages(include=['crlf']),
      entry_points={
          'console_scripts': ['crlf=crlf.__main__:main'],
      })
