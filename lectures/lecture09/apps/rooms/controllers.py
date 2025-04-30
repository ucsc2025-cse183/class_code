from py4web import URL, abort, action, redirect, request
from .common import auth, db
from py4web.utils.form import Form

@action("index")
@action.uses("generic.html")
def index():
    return {"message": "hello to room reservations app"}

@action("register_room")
@action.uses("generic.html", auth.user)
def register_room():    
    form = Form(db.room)  # Create Form
    return locals()

@action("edit_room/<room_id>")
@action.uses("generic.html", auth.user)
def register_room(room_id):
    form = Form(db.room, room_id) # Update form 
    return locals()

@action("list_rooms")
@action.uses("list_rooms.html", auth.user)
def list_rooms():
    rows = db(db.room).select() # Selecting rooms
    return locals()

@action("make_reservation")
@action.uses("generic.html", auth.user)
def make_reservation():
    return locals()

@action("list_my_reservations")
@action.uses("generic.html", auth.user)
def list_my_reservations():
    return locals()          

