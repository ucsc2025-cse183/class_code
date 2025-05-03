from pydal.validators import *
from .common import Field, db

db.define_table(
    "room",
    Field("name", requires=IS_NOT_EMPTY()),
    Field("location", requires=IS_NOT_EMPTY()),
    Field("size", "integer", requires=IS_INT_IN_RANGE(1,1000)),
)

db.define_table(
    "reservation",
    Field("room_id", "reference room"),
    Field("user_id", "reference auth_user"),
    Field("start_datetime", "datetime"),
    Field("stop_datetime", "datetime")
)

# db(db.room).delete()
#if (db(db.room).count() == 0):
#    db.room.insert(
#        name="Room1",
#        size="5",
#        location="Main Campus - 101 Main St - 3rd floor"
#    )

# db(db.reservation).delete()

db.commit()