"""
This file defines the database models
"""

from pydal.validators import *

from .common import Field, db


db.define_table("fruit", Field("name"))

db.commit()