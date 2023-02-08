#!/usr/bin/env python3
from setuptools import setup, find_packages

from crlf import __version__

setup(name='crlf',
      version=__version__,
      packages=find_packages(include=['crlf']),
      entry_points={
          'console_scripts': ['crlf=crlf.__main__:start'],
      })
