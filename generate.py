# coding: utf-8

import os
import json

from jinja2 import Environment, PackageLoader

from sqlalchemy.ext.declarative.api import DeclarativeMeta

DB_URI = os.getenv('TEST_DB_URI')

invalid = ['Base', 'models_module']

cwd = os.getcwd()
env = Environment(
    loader=PackageLoader('api', ''),
    trim_blocks=True,
    lstrip_blocks=True)


def field_2_factory_func(field):
    """Convert a sqlalchemy field into a corresponding factory boy function.

    These functions are used as LazyAttribute functions that are
    pre-defined in `factories.py`
    """
    field = repr(field)
    return ''
    if 'sql.sqltypes.Text' in field or 'sql.sqltypes.String' in field:
        return 'rand_str'
    elif 'sql.sqltypes.Date' in field:
        return 'new_date'
    elif 'sql.sqltypes.BigInteger' in field:
        return 'rand_int'
    elif 'sql.sqltypes.SmallInteger' in field:
        return 'rand_int'
    elif 'sql.sqltypes.Integer' in field:
        return 'rand_int'
    else:
        print('COULD NOT FIND MAPPING!')
    return ''


def get_model_detail(models, module):
    """Take generated models, extract their fields and field types."""
    models_detailed = []
    gencls = 'api.generated.models'
    # Get the appropriate models.
    module = {k: v for k, v in globals().items() if gencls in repr(v)}
    for name, klass in module.items():
        fields = {
            k: v for k, v in vars(klass).items() if not k.startswith('__')
        }
        fields = {
            name: field_2_factory_func(val) for name, val in fields.items()
        }
        models_detailed.append(dict(name=name, klass=klass, fields=fields))
    return models_detailed


if __name__ == '__main__':
    os.system('rm -rf {}/api/generated'.format(cwd))
    os.system('mkdir {}/api/generated'.format(cwd))

    os.system('sqlacodegen {db} > api/generated/models.py'.format(db=DB_URI))

    with open('api/generated/__init__.py', 'wb') as app:
        app.write('\n')

    # One the init file above is created, we can import the generated models
    # as a module here to extract the class names.

    # Put class names in this namespace with globals()
    from api.generated import models as models_module
    from api.generated.models import *

    models = list(set([
        obj.__name__ for k, obj in globals().items()
        if isinstance(obj, DeclarativeMeta) and obj.__name__ not in invalid
    ]))
    jsonconfig = dict(
        app='myapp',
        db_uri=DB_URI,
        debug=True,
        models=models,
    )

    with open('api/generated/app.py', 'wb') as app:
        app.write(env.get_template('app.py').render(**jsonconfig))

    with open('api/generated/sessions.py', 'wb') as app:
        app.write(env.get_template('sessions.py').render(**jsonconfig))

    with open('api/generated/factories.py', 'wb') as app:
        app.write(env.get_template('factories.py').render(**dict(
            models=get_model_detail(models, models_module))))
