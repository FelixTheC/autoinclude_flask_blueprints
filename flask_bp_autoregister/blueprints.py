#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 12.05.20
@author: eisenmenger
"""
import os
import pathlib
from typing import Union
from strongtyping.strong_typing import match_typing

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
    if path_length >= 1 and bp_module[0][0] != '#':  # ignore blueprints when they are comment out
        try:
            # imports module dynamically
            module = __import__(bp_module[1], fromlist=[bp_module[0], ])
        except ModuleNotFoundError:
            return get_module_blueprint((bp_module[0], '.'.join(bp_module[1].split('.')[1:])))
        else:
            # returns the created Blueprint instance from the dynamically imported module
            try:
                return getattr(module, bp_module[0])
            except AttributeError:
                return get_module_blueprint((bp_module[0], '.'.join(bp_module[1].split('.')[1:])))


def register_blueprint_4_flask_app(flask_app: flask.app.Flask, blueprint: flask.Blueprint, silent: bool, *args):
    try:
        flask_app.register_blueprint(blueprint)
    except AttributeError as e:
        error_info = ('Found disabled/broken Blueprint', *args)
        if silent:
            print(error_info)
        else:
            raise AttributeError(error_info)


@match_typing
def add_blueprints_from_dir(*, directory: pathlib.Path = None, flask_app: flask.app.Flask = None, silent: bool = False):
    files_and_bps = []
    for file in directory.glob('**/*.py'):
        if file.name != __file__:
            file_lines = file.open().readlines()
            files_and_bps.extend([(get_blueprint_name(line),
                                   path_url_2_model_path(file.as_posix())
                                   ) for line in file_lines if is_blueprint_line(line)
                                  ])

    [register_blueprint_4_flask_app(flask_app, get_module_blueprint(f_bp), silent, f_bp) for f_bp in files_and_bps]


@match_typing
def register_blueprints(used_flask_app: flask.app.Flask, base_path: str = None, silent: bool = False) -> None:
    """
    :param used_flask_app: the flask app "flask_app = Flask(__name__)"
    :param base_path: the path from the base dir like "my_app/src/api"
    :param silent: False if errors during the registration should be raised True if they only should be printed
    """
    bp_dir = pathlib.Path(base_path) if base_path is not None else pathlib.Path(used_flask_app.root_path)
    add_blueprints_from_dir(directory=bp_dir,
                            flask_app=used_flask_app,
                            silent=silent)
