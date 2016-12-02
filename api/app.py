# coding: utf-8

"""A RESTFUL API for {{ app }}."""

from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
import flask_restless
from flask_restful import Api

# First-party
import models
from sessions import SESSION, ENGINE

app = Flask('{{ app }}')
app.debug = {{ debug }}
api = Api(app)
manager = flask_restless.APIManager(app, session=SESSION)

# Setup Migrations
migrate = Migrate(app, ENGINE)

# Setup script Manager
script_manager = Manager(app)
script_manager.add_command('db', MigrateCommand)

api_options = dict(
    methods=['GET', 'POST', 'PATCH', 'DELETE', 'PUT'],
    results_per_page=100,
)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
# Create the Flask-Restless API manager.
{% for model in models %}
manager.create_api(models.{{ model }}, **api_options)
{% endfor %}

if __name__ == '__main__':
    script_manager.run()

