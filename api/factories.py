# coding: utf-8

"""Model Factories for generating data, fake or otherwise."""

from __future__ import absolute_import
from random import choice, randrange
from datetime import datetime as dt
import os
import json

import factory
from faker import Faker

import models
import sessions

faker = Faker()


def rand_bool(*args):
    """Return a random boolean."""
    return choice([True, False])


def rand_name(*args):
    """Return a random title, first and last name."""
    return faker.name()


def new_date(*args):
    """Return a random datetime now string."""
    return dt.now()


def generate_data(engine, dbsession, total=10):
    """Generate workflows and jobs.

    You must pass your own engine and session.
    """
    # Create tables
    bm.Base.metadata.create_all(engine)
    for _ in range(total):
        {% for model in models %}
            {{ model }}.create()
        {% endfor %}
    dbsession.commit()


{% for model in models %}
class {{ model.name }}Factory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating a {{ model.name }}."""

    class Meta:
        """Metaclass."""

        model = models.{{ model.name }}
        sqlalchemy_session = sessions.SESSION

    {% for attr, factory_name in model.fields.items() %}
    {{ attr }} = factory.LazyAttribute({{ factory_name }})
    {% endfor %}


{% endfor %}
