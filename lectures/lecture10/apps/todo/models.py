"""
This file defines the database models
"""

from pydal.validators import *

from .common import Field, db

db.define_table("todo",
    Field("description", requires=IS_NOT_EMPTY())
)

if db(db.todo).count() == 0:
    db.todo.insert(description="clean")
    db.todo.insert(description="wash")
    db.todo.insert(description="shower")

db.commit()    