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


register_blueprints(flask_app, 'my_project/src/my_app') # the root directory under which all blueprints are created


if __name__ == '__main__':
    flask_app.run()

```

### Tested for Versions
- 3.6, 3.7, 3.8

### Installing

- pip install git+https://github.com/FelixTheC/flask_bp_autoregister.git

#### Versioning
- For the versions available, see the tags on this repository.

### Authors
- Felix Eisenmenger - Initial work

### License
- This project is licensed under the MIT License - see the LICENSE.md file for details
