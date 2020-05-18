#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 18.05.20
@author: felix
"""
import os
import pathlib

import flask


def is_blueprint_line(line: str):
    return 'Blueprint' in line


def get_blueprint_name(line: str):
    return line.split('=')[0].strip()


def path_url_2_model_path(path: str):
    return ''.join(path.split('/src')[-1])[1:].replace(os.path.sep, '.').replace('.py', '')


def get_module_blueprint(bp_module: tuple) -> flask.Blueprint:
    module = __import__(bp_module[1], fromlist=[bp_module[0], ])
    return getattr(module, bp_module[0])


def add_blueprints_from_dir(*, directory: pathlib.Path = None, flask_app: any = None):
    files_and_bps = []
    for file in directory.glob('**/*.py'):
        file_lines = file.open().readlines()
        files_and_bps.extend([(get_blueprint_name(line),
                               path_url_2_model_path(file.as_posix())) for line in file_lines if is_blueprint_line(line)
                              ])
    [flask_app.register_blueprint(get_module_blueprint(f_bp)) for f_bp in files_and_bps]