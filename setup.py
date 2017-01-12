#!/usr/bin/env python
from setuptools import setup, find_packages

if __name__ == '__main__':
   setup(name='logstasher',
         version='0.1.4',
         description='Threaded logstash handler and formatter',
         url='https://github.com/meltwater/threaded-logstasher',
         author='Knowledgebase Team',
         author_email='det.kgb@meltwater.com',
         packages=find_packages(),
         install_requires=['logstash_formatter==0.5.14'],
         license=None,
         zip_safe=False)
