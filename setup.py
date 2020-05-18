#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 18.05.20
@author: felix
"""
import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setuptools.setup(
    name="autoinclude_blueprints",
    version="0.3",
    author="Felix Eisenmenger",
    author_email="f.eisenmenger@gmx.net",
    description="A package for flask to auto include Blueprints",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/FelixTheC/autoinclude_flask_blueprints.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
    ],
    packages=['incl_blueprints'],
    include_package_data=True,
)
