#! /usr/bin/env python3

from setuptools import find_packages, setup

setup(name="python-lcomp",
      version="0.2",
      description="L-CARD ADC/DAC controllers library",
      url="https://github.com/RAA80/python-lcomp",
      author="Alexey Ryadno",
      author_email="aryadno@mail.ru",
      license="MIT",
      packages=find_packages(),
      package_data={"lcomp": ["bios/*.pld", "bios/*.bio",
                              "libs/*.dll", "libs/*.so"]},
      install_requires=["numpy >= 1.20"],
      platforms=["Linux", "Windows"],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Science/Research",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: Microsoft :: Windows",
                   "Operating System :: POSIX :: Linux",
                   "Operating System :: POSIX",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.9",
                   "Programming Language :: Python :: 3.10",
                   "Programming Language :: Python :: 3.11",
                  ],
     )
