"""Session setup for accessing models for {{ app }}"""

from __future__ import absolute_import
from contextlib import contextmanager
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URI = '{{ db_uri }}'
ENGINE = create_engine(DB_URI, echo={{ debug }})
SESSION = scoped_session(sessionmaker(bind=ENGINE))


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of db operations."""
    _session = SESSION()
    try:
        yield _session
        _session.commit()
    except:
        _session.rollback()
        raise
    finally:
        _session.close()
