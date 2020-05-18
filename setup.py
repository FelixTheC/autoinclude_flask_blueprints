#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 18.05.20
@author: felix
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoinclude_flask_blueprints-FelixTheC",
    version="0.0.1",
    author="Felix Eisenmenger",
    author_email="f.eisenmenger@gmx.net",
    description="A package for flask to auto include Blueprints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FelixTheC/autoinclude_flask_blueprints.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
    ],
    python_requires='>=3.6',

)
