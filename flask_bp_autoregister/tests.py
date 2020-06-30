#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 26.06.20
@author: felix
"""
import pathlib
import sys

import flask
import pytest
from flask_bp_autoregister.blueprints import register_blueprints


def account_view_blueprint() -> str:
    return """
import flask

app_bp = flask.Blueprint('account', __name__, url_prefix='/account')

@app_bp.route('/')
def index():
    return 'Success'
    
"""


def create_sample_text_2() -> str:
    return """
from dataclasses import dataclass


@dataclass
class alias:  # no pep8

    attr_name: str
    write: bool = False

    def __get__(self, instance, owner):
        obj = instance if instance is not None else owner
        return getattr(obj, self.attr_name)

    def __set__(self, instance, value):
        if self.write:
            setattr(instance, self.attr_name, value)
        else:
            raise AttributeError
        
"""


def home_view_blueprint():
    return """
    
from datetime import datetime
import flask
from flask.views import View, MethodView

app_bp = flask.Blueprint('home', __name__, template_folder='templates')


def get_dummy_packages():
    return [
        {
            'name': 'flask',
            'version': '1.2.3'
        }, {
            'name': 'sqlalchemy',
            'version': '2.2.0'
        }, {
            'name': 'passlib',
            'version': '3.0.0'
        },
    ]


class IndexView(MethodView):
    template_file = 'index.html'

    def get(self):
        return str({'packages': get_dummy_packages()})


class AboutView(MethodView):
    template_file = 'about.html'
    
    def get(self):
        print(f'get called: {datetime.today()}')
        return 'Some About info'


app_bp.add_url_rule('/', view_func=IndexView.as_view(name='index'))
app_bp.add_url_rule('/about', view_func=AboutView.as_view(name='about'))
    
    """


def account_view_comment_blueprint() -> str:
    return """
import flask

# app_bp = flask.Blueprint('account', __name__, url_prefix='/account')

@app_bp.route('/')
def index():
    return 'Success'
    
"""


def account_view_commented_file() -> str:
    return """
import flask

# app_bp = flask.Blueprint('account', __name__, url_prefix='/account')

# @app_bp.route('/')
# def index():
#     return 'Success'
    
"""


def add_tmp_path_to_sys(path: pathlib.Path):
    if path not in sys.path:
        sys.path[0] = str(path)


def add_init_py(path: pathlib.Path) -> pathlib.Path:
    path = path / '__init__.py'
    path.write_text('\n')
    return path.parent


@pytest.fixture(autouse=True)
def create_tmp_project_struct(tmp_path):
    d = tmp_path / 'my_app'
    d.mkdir()
    d = d / 'src'
    d.mkdir()
    d = add_init_py(d)
    add_tmp_path_to_sys(d)
    d = d / 'app'
    d.mkdir()
    d = add_init_py(d)
    d = d / 'some_view'
    d.mkdir()
    d = add_init_py(d)
    d = d / 'some_api.py'
    d.write_text(account_view_blueprint())
    d = d.parent / 'some_utils.py'
    d.write_text(create_sample_text_2())
    d = d.parent.parent / 'other_view'
    d.mkdir()
    d = add_init_py(d)
    d = d / 'api'
    d.mkdir()
    d = add_init_py(d)
    d = d / 'api_api'
    d.mkdir()
    d = d / 'api_api_api'
    d.mkdir()
    d = d / 'other_api.py'
    d.write_text(home_view_blueprint())
    return d


@pytest.fixture(autouse=True)
def create_broken_project_struct(tmp_path):
    d = tmp_path / 'my_other_app'
    d.mkdir()
    d = d / 'src'
    d.mkdir()
    d = d / 'app'
    d.mkdir()
    d = d / 'some_view'
    d.mkdir()
    d = d / 'some_api.py'
    d.write_text(account_view_comment_blueprint())
    return d


@pytest.fixture(autouse=True)
def create_disabled_project_struct(tmp_path):
    d = tmp_path / 'my_disabled_app'
    d.mkdir()
    d = d / 'src'
    d.mkdir()
    d = d / 'app'
    d.mkdir()
    d = d / 'some_view'
    d.mkdir()
    d = d / 'some_api.py'
    d.write_text(account_view_commented_file())
    return d


def test_find_all_blueprints(create_tmp_project_struct):
    flask_app = flask.Flask(__name__)
    register_blueprints(flask_app, str(tuple(create_tmp_project_struct.parents)[5]))
    assert len(flask_app.blueprints) == 2
    assert 'home' in flask_app.blueprints
    assert 'account' in flask_app.blueprints


def test_find_only_home_blueprints(create_tmp_project_struct):

    flask_app = flask.Flask(__name__)
    # path => 'my_app/src/app/other_view'
    register_blueprints(flask_app, str(tuple(create_tmp_project_struct.parents)[1]))
    assert len(flask_app.blueprints) == 1
    assert 'home' in flask_app.blueprints
    assert 'account' not in flask_app.blueprints


def test_find_only_account_blueprints(create_tmp_project_struct):

    flask_app = flask.Flask(__name__)
    # path => 'my_app/src/app/some_view'
    register_blueprints(flask_app, str(tuple(create_tmp_project_struct.parents)[4] / 'some_view'))
    assert len(flask_app.blueprints) == 1
    assert 'home' not in flask_app.blueprints
    assert 'account' in flask_app.blueprints


def test_ignore_commented_blueprints(create_broken_project_struct):
    flask_app = flask.Flask(__name__)
    with pytest.raises(AttributeError):
        register_blueprints(flask_app, str(tuple(create_broken_project_struct.parents)[1]))


def test_ignore_silent_commented_blueprints(create_broken_project_struct):
    flask_app = flask.Flask(__name__)
    register_blueprints(flask_app, str(tuple(create_broken_project_struct.parents)[2]), silent=True)
    assert len(flask_app.blueprints) == 0


def test_base_path_empty(create_tmp_project_struct, tmp_path):
    d = tmp_path / 'my_app' / 'src' / 'app'
    flask_app = flask.Flask(__name__)
    flask_app.root_path = str(d)
    register_blueprints(flask_app)
    assert len(flask_app.blueprints) == 2


def test_disabled_file(create_disabled_project_struct, tmp_path):
    d = tmp_path / 'my_disabled_app' / 'src' / 'app'
    flask_app = flask.Flask(__name__)
    flask_app.root_path = str(d)
    register_blueprints(flask_app, silent=True)
    assert len(flask_app.blueprints) == 0


if __name__ == '__main__':
    pytest.main(['-vv', '-s', __file__])
