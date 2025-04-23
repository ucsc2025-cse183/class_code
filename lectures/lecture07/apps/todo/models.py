from pydal.validators import *
from .common import Field, db

db.define_table(
    "item",
    Field("description", requires=IS_NOT_EMPTY()),
    Field("deadline", "datetime"),
    Field("done", "boolean", label="completed?")
)