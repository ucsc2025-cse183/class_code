"""
This file defines the database models
"""

from pydal.validators import *
from py4web.utils.populate import populate
from .common import Field, db

db.define_table('thing', Field('name'))

if db(db.thing).count() == 0:
    populate(db.thing, 100)

db.commit()    