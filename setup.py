#! /usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup


setup(name="python-lcomp",
      version='0.0.27',
      description='L-CARD ADC/DAC controller module',
      url='https://github.com/RAA80/python-lcomp',
      author='Ryadno Alexey',
      author_email='aryadno@mail.ru',
      license='MIT',
      packages=['lcomp', 'lcomp.device', 'lcomp.libs', 'lcomp.bios'],
      package_data={"lcomp": ["bios/*.pld", "bios/*.bio",
                              "libs/*.dll", "libs/*.so"]},
      install_requires=['numpy >= 1.12'],
      platforms=['Linux', 'Mac OS X', 'Windows'],
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: POSIX',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                  ]
     )
