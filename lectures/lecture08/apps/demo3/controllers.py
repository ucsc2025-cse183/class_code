
from yatl.helpers import A
from py4web import URL, abort, action, redirect, request
from .common import (T, auth, authenticated, cache, db, flash, logger, session,
                     unauthenticated)


@action("index")
@action.uses("index.html", auth, T)
def index():
    user = auth.get_user()
    message = T("Hello {first_name}").format(**user) if user else T("Hello")
    return dict(message=message)
