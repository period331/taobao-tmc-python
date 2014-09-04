# coding: utf-8
from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='taobao-tmc-py',
      version=version,
      description="淘宝平台消息服务python版本",
      long_description="""
taobao-tmc-python
=======================

淘宝平台消息服务python版本

usage:
```python
logging.basicConfig(level=logging.DEBUG)
ws = TmcClient('ws://mc.api.tbsandbox.com/', 'appkey', 'appsecret', 'default',
    query_message_interval=50)
def print1():
    print 'on_open'
ws.on("on_open", print1)
try:
    ioloop.IOLoop.instance().start()
except KeyboardInterrupt:
    pass
finally:
    ws.close()
```

""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='taobao tmc python',
      author='baocaixiong',
      author_email='baocaixiong@gmail.com',
      url='https://github.com/baocaixiong/taobao-tmc-python',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'tornado==4.0'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
