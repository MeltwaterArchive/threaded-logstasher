#!/usr/bin/env python
from setuptools import setup, find_packages

if __name__ == '__main__':
   setup(name='logstasher',
         version='0.1.4',
         description='Threaded logstash handler and formatter',
         url='https://github.com/meltwater/threaded-logstasher',
         author='Gyozo Papp',
         author_email='gyozo.papp@meltwater.com',
         packages=find_packages(),
         install_requires=['logstash_formatter==0.5.14'],
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
