from py4web import URL, abort, action, redirect, request
from .common import auth

@action("index")
@action.uses("generic.html", auth)
def index():
    return {"a": 1}
