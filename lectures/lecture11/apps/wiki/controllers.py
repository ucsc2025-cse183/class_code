from py4web import URL, abort, action, redirect, request
from .common import auth, db
import re


@action("index")
@action.uses("index.html", auth)
def page():
    return dict()


@action("page/new")
@action.uses("page.html", auth.user)
def page():
    return dict()

@action("page/<page_id:int>")
@action.uses("page.html", auth)
def page(page_id=None):
    return dict()

# /page/ -> a list of all pages
@action("api/page", method="GET")
@action.uses(auth)
def get_page():
    pages = db(db.page).select(db.page.id,db.page.title,orderby=db.page.title)
    return {"pages": pages, "user_id": auth.user_id}

# /page/<page_id> -> a page
@action("api/page/<page_id:int>", method="GET")
@action.uses(auth)
def get_page(page_id):
    page = db(db.page.id==page_id).select().first()
    if not page:
        raise HTTP(404)
    page.created_by_first_name = page.created_by.first_name
    return {"page": page}

# POST to /page -> create the page and return the id
@action("api/page", method="POST")
@action.uses(auth.user)
def post_page():
    ret = db.page.validate_and_insert(**request.json)
    return ret

# PUT to /page/<page_id> -> update the page
@action("api/page/<page_id:int>", method="PUT")
@action.uses(auth.user)
def put_page(page_id):
    page = db.page(page_id)
    if not page:
        raise HTTP(404)
    if page.created_by != auth.user_id:
        return {"errors": "not allowed"}
    ret = db.page.validate_and_update(page_id, **request.json)
    return ret

# DELETE a /page/<page_id> -> deletes the page
@action("api/page/<page_id:int>", method="DELETE")
@action.uses(auth.user)
def delete_page(page_id):
    num = db((db.page.id == page_id)&(db.page.created_by == auth.user_id)).delete()
    return {"num_delete": num}

# /page/<page_id>/comment -> comments for the page
@action("api/page/<page_id:int>/comment", method="GET")
@action.uses(auth)
def get_comments(page_id):
    page = db.page(page_id)
    if not page:
        raise HTTP(404)
    comments = db(db.comment.page_id==page_id).select()  ## SQL select
    user_ids = set([comment.created_by for comment in comments])
    users = db(db.auth_user.id.belongs(user_ids)).select(db.auth_user.id, db.auth_user.first_name).as_dict()  ## SQL select
    for comment in comments:
        comment.created_by_first_name = users[comment.created_by]["first_name"]
    print(users)
    return {"comments": comments.as_list()}

# POST to /page/<page_id>/comment -> create the comment the page id
@action("api/page/<page_id:int>/comment", method="POST")
@action.uses(auth.user)
def post_comment(page_id):
    page = db.page(page_id)
    if not page:
        raise HTTP(404)
    db.comment.page_id.default = page_id
    ret = db.comment.validate_and_insert(**request.json) # {errors: [], id: 1}
    return ret
