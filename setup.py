#!/usr/bin/env python3

import setuptools
from bonbast import VERSION

readme_f = open('README.md', 'r')
long_description = readme_f.read()
readme_f.close()

setuptools.setup(
    name="bonbast",
    version=VERSION,
    author="Amir SamadiPour",
    author_email="samadipour@gmail.com",
    description="", # TODO : Add short description
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SamadiPour/bonbast",
    packages=setuptools.find_packages(),
    scripts=['bin/bonbast'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        #"License :: OSI Approved :: MIT License" # TODO : Set the valid license
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests >= 2.28.0",
        "rich >= 12.4.4",
    ]
)
