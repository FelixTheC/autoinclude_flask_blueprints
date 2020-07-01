![Upload Python Package](https://github.com/FelixTheC/autoinclude_flask_blueprints/workflows/Upload%20Python%20Package/badge.svg?branch=master)
![Python application](https://github.com/FelixTheC/autoinclude_flask_blueprints/workflows/Python%20application/badge.svg?branch=master)
# Flask Blueprint autoinclude
A function to automatically register all flask-blueprints from a project.
<br>__register_blueprints__ from flask_bp_autoregister.blueprints

---
When using flask blueprints then after defining them you have to register them all this can possible look like this.
```python
# in some config.py or __init__.py
def register_my_blueprints(used_flask_app: any):
    from my_app.views import home_views
    from my_app.views import package_views
    from my_app.views import account_views
    
    used_flask_app.register_blueprint(home_views.app_bp)
    used_flask_app.register_blueprint(package_views.app_bp)
    used_flask_app.register_blueprint(account_views.app_bp) 

# and then in your run.py or similar

from my_app import flask_app
from my_app import register_my_blueprints

register_my_blueprints(flask_app)

if __name__ == '__main__':
    flask_app.run()

```
The register_blueprints code can get really long and you always have to remember where your blueprints are.

---

For this is had created a function __register_blueprints__ which automatically will search for all blueprints in your project and register them.
```python

from my_app import flask_app
from flask_bp_autoregister.blueprints import register_blueprints


register_blueprints(flask_app, 'my_project/src/my_app')


if __name__ == '__main__':
    flask_app.run()

```

The path attribute is not really needed you can also use it without then all blueprints inside of the project will be registered automatically
```python

from my_app import flask_app
from flask_bp_autoregister.blueprints import register_blueprints


register_blueprints(flask_app)


if __name__ == '__main__':
    flask_app.run()

```

When you have some __commented Blueprints__ inside of your project, __register_blueprints__ will try to register them too <br>
which will raise an AttributeError you can disable this with __silent=True__
```python
from my_app import flask_app
from flask_bp_autoregister.blueprints import register_blueprints


register_blueprints(flask_app, silent=True) # will prevent raising AttributeError


if __name__ == '__main__':
    flask_app.run()

```

### Tested for Versions
- 3.6, 3.7, 3.8

### Installing

- pip install git+https://github.com/FelixTheC/autoinclude_flask_blueprints.git

#### Versioning
- For the versions available, see the tags on this repository.

### Authors
- Felix Eisenmenger - Initial work

### License
- This project is licensed under the MIT License - see the LICENSE.md file for details
