#!/usr/bin/env python
from setuptools import setup, find_packages
import codecs
import os.path

def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts),
                       encoding="utf-8").read()

if __name__ == '__main__':
   setup(name='logstasher',
         version='0.1.5',
         description='Threaded logstash handler and formatter',
         long_description=read('README.md'),
         url='https://github.com/meltwater/threaded-logstasher',
         author='Gyozo Papp',
         author_email='gyozo.papp@meltwater.com',
         packages=find_packages(),
         install_requires=['logstash_formatter==0.5.14'],
         keywords='logging logstash threaded',
         license='BSD',
         classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3'
         ],
         zip_safe=False)
