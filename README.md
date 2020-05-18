# Auto include blueprints from a directory


## Getting Started
Example:
 
<p>src/app/__init__.py</p>

```
def register_blueprints(used_flask_app: any):
    current = pathlib.Path.cwd()
    add_blueprints_from_dir(directory=pathlib.Path.joinpath(current, 'src', 'app', 'views'),
                            flask_app=used_flask_app)
```
And in your src/run.py
```
...
from app import flask_app
from app import register_blueprints
...

register_blueprints(flask_app)

...

if __name__ == '__main__':
    flask_app.run()
```


### Prerequisites
- flask

### Installing
- python setup.py install
- https://github.com/FelixTheC/autoinclude_flask_blueprints.git

### Running the tests
- python test_typing.py

#### Versioning
- For the versions available, see the tags on this repository.

### Authors
- Felix Eisenmenger - Initial work

### License
- This project is licensed under the MIT License - see the LICENSE.md file for details