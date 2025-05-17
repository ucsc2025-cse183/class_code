from pydal.validators import *
from .common import Field, db, auth

db.define_table(
    "page",
    Field("title", "string"), # requires=IS_NOT_IN_DB(db, "page.title")),   
    Field("content", "text", requires=IS_NOT_EMPTY()),
    auth.signature
    ) # content, author, timestamp

db.define_table(
    "comment",
    Field("page_id", "reference page", writable=False),
    Field("content", "text"),
    auth.signature
) # content, author, timestamp

db.commit()