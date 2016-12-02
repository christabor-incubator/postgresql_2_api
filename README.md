# postgresql_2_api
A toolset to introspect raw postgresql schemas and genenrate them into a fully functioning flask REST api in a single command.

## Getting started

### Install requirements

Relies on: `flask-restless`, `sqlacodegen`, `jinja2`, `sqlalchemy` and any of these libraries' dependencies.

### Run commands

1. export your DB uri as `TEST_DB_URI` (for now). (e.g. `export TEST_DB_URI=postgresql://username:pass@0.0.0.0:5432/dbname`)
2. Run `generate.py`
3. Start the app! `python api/generated/app.py`

This is just for testing. You can move it elsewhere and refactor or change anything. But this gets you up and running immediately.
