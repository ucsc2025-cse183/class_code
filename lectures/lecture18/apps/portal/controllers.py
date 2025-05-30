from py4web import URL, abort, action, redirect, request
from py4web.utils.form import Form
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
    groups
)


@action("index")
@action.uses("generic.html", auth)
def index():
    message = "Hey you are on the index page!"
    return locals()


@action("admin_only")
@action.uses("generic.html", auth.user)
def index():
    if not db(groups.find("admin")&(db.auth_user.id==auth.user_id)).count():
        auth.flash.set("You were not allowed to see that!")
        redirect(URL("index"))
    message = "You are authorized"
    return locals()


@action("make_admin", method="POST")
@action.uses(auth.user)
def index():
    if auth.user_id is not 1:
        raise HTTP(400)
    user_id = request.json.get("user_id")
    groups.add(user_id, "admin")
    return {}


@action("create_fruit")
@action.uses("generic.html", auth)
def index():
    form = Form(db.fruit)
    if form.accepted:
        auth.flash.set("Record was inserted")
        redirect(URL("index"))
    elif form.errors:
        auth.flash.set("Oops! something was wrong")
    return locals()

