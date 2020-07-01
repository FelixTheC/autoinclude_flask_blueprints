#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 30.04.20
@author: felix
"""
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
setup(
    name="autoinclude_blueprints",
    version="1.0.1",
    description="Auto register all project flask-blueprints.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/FelixTheC/flask_bp_autoregister",
    author="FelixTheC",
    author_email="fberndt87@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=['flask_bp_autoregister'],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        "flask>=1.1.0",
        "strongtyping>=1.3.0"
    ]
)
