#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 12.05.20
@author: eisenmenger
"""
import os
import pathlib
from typing import Union

import flask


class BlueprintPathError(Exception):
    pass


def is_blueprint_line(line: str):
    return 'Blueprint' in line


def get_blueprint_name(line: str):
    return line.split('=')[0].strip()


def path_url_2_model_path(path: str):
    path = path[1:] if path[0] == os.path.sep else path
    return path.replace(os.path.sep, '.').replace('.py', '')


def get_module_blueprint(bp_module: tuple) -> Union[flask.Blueprint, None]:
    """
    :param bp_module: (variable_name, module_path) => ('app_bp', 'src.app.views.account_views')
    :return: flask.blueprints.Blueprint object
    """
    path_length = len(bp_module[1])
    if path_length >= 1:
        try:
            # imports module dynamically
            module = __import__(bp_module[1], fromlist=[bp_module[0], ])
        except ModuleNotFoundError as e:
            return get_module_blueprint((bp_module[0], '.'.join(bp_module[1].split('.')[1:])))
        else:
            # returns the created Blueprint instance from the dynamically imported module
            try:
                return getattr(module, bp_module[0])
            except AttributeError:
                return get_module_blueprint((bp_module[0], '.'.join(bp_module[1].split('.')[1:])))


def add_blueprints_from_dir(*, directory: pathlib.Path = None, flask_app: any = None):
    files_and_bps = []
    for file in directory.glob('**/*.py'):
        if file.name != __file__:
            file_lines = file.open().readlines()
            files_and_bps.extend([(get_blueprint_name(line),
                                   path_url_2_model_path(file.as_posix())
                                   ) for line in file_lines if is_blueprint_line(line)
                                  ])
    [flask_app.register_blueprint(get_module_blueprint(f_bp)) for f_bp in files_and_bps if f_bp is not None]


def register_blueprints(used_flask_app: any, base_path: str = None):
    bp_dir = pathlib.Path(base_path) if base_path is not None else pathlib.Path(__file__).resolve().parent
    add_blueprints_from_dir(directory=bp_dir,
                            flask_app=used_flask_app)
