from pydal.validators import *
from .common import Field, db

db.define_table("color", Field('name'))

