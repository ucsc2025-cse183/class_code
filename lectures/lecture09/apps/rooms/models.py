from pydal.validators import *
from .common import Field, db

db.define_table(
    "room",
    Field("name"),
    Field("location"),
    Field("size", "integer"),    
)

# db(db.room).delete()
#if (db(db.room).count() == 0):
#    db.room.insert(
#        name="Room1",
#        size="5",
#        location="Main Campus - 101 Main St - 3rd floor"
#    )

db.commit()