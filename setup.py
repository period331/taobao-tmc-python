# coding: utf-8
from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='taobao-tmc-py',
      version=version,
      description="淘宝平台消息服务python版本",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='taobao tmc python',
      author='baocaixiong',
      author_email='baocaixiong@gmail.com',
      url='baocaixiong.github.io',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'tornado==4.0.0'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
