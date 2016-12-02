# coding: utf-8

import os
import json

from jinja2 import Environment, PackageLoader

from sqlalchemy.ext.declarative.api import DeclarativeMeta

DB_URI = os.getenv('TEST_DB_URI')

invalid = ['Base']

cwd = os.getcwd()
env = Environment(
    loader=PackageLoader('api', ''),
    trim_blocks=True,
    lstrip_blocks=True)

if __name__ == '__main__':
    os.system('rm -rf {}/api/generated'.format(cwd))
    os.system('mkdir {}/api/generated'.format(cwd))

    os.system('sqlacodegen {db} > api/generated/models.py'.format(db=DB_URI))

    with open('api/generated/__init__.py', 'wb') as app:
        app.write('\n')

    # One the init file above is created, we can import the generated models
    # as a module here to extract the class names.

    # Put class names in this namespace with globals()
    from api.generated.models import *

    jsonconfig = dict(
        app='myapp',
        db_uri=DB_URI,
        debug=True,
        models=list(set([
            obj.__name__ for k, obj in globals().items()
            if isinstance(obj, DeclarativeMeta) and obj.__name__ not in invalid
        ]))
    )

    with open('api/generated/app.py', 'wb') as app:
        app.write(env.get_template('app.py').render(**jsonconfig))

    with open('api/generated/sessions.py', 'wb') as app:
        app.write(env.get_template('sessions.py').render(**jsonconfig))
