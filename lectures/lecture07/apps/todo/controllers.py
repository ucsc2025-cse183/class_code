from py4web import URL, action, redirect, request
from .common import (T, auth, authenticated, cache, db, flash, logger, session,
                     unauthenticated)
from py4web.utils.form import Form

@action("index")
@action.uses("test.html", auth, T)
def index():
    form = Form(db.item)
    rows = db(db.item).select()
    return {"rows": rows, "form": form}
