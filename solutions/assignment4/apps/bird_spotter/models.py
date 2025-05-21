# uncomment the following and add your model
from pydal.validators import *
from .common import Field, db

db.define_table(
    "bird",
    Field("name", notnull=True, requires=IS_NOT_IN_DB(db, "bird.name")),
    Field("habitat", default=""),
    Field("weight", "float", default=0, requires=IS_FLOAT_IN_RANGE(0, 1000)),
    Field("sightings", "integer", default=0),
)

db.commit()
