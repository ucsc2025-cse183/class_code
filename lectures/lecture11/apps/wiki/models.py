from pydal.validators import *
from py4web.utils.populate import populate
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

if db(db.auth_user).count()>0 and db(db.page).count() < 10:
    populate(db.page, 100)
    populate(db.comment, 300)

db.commit()