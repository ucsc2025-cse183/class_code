from pydal.validators import *
from .common import Field, db

db.define_table(
    "page",
    Field("title", "string", requires=IS_NOT_IN_DB(db, "page.title")),   
    Field("content", "text", requires=IS_NOT_EMPTY()),
    Field("author_id", "reference auth_user", writable=False),
    ) # content, author, timestamp

db.define_table(
    "comment",
    Field("page_id", "reference page", writable=False),
    Field("content", "text"),
    Field("author_id", "reference auth_user", writable=False),
) # content, author, timestamp

if db(db.page).count() == 0:
    db.page.insert(
        title="my first page",
        content="nothing to say",
        author_id=1
    )

db.commit()