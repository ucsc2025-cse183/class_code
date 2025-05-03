
from yatl.helpers import A

from py4web import URL, abort, action, redirect, request

from .common import (
    T,
    auth,
    authenticated,
    cache,
    db,
    flash,
    logger,
    session,
    unauthenticated,
)


@action("index")
def index():
    redirect(URL("static/index.html"))

@action("record_todo")
@action.uses(db)
def record_todo():
    return db.todo.validate_and_insert(**request.json)

@action("list_todos")
@action.uses(db)
def list_todos():
    rows = db(db.todo).select().as_list()
    return {"rows": rows} 