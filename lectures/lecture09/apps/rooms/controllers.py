from pydal.validators import IS_DATETIME
from py4web import URL, abort, action, redirect, request, Field
from .common import auth, db
from py4web.utils.form import Form
import datetime

@action("index")
@action.uses("generic.html", auth)
def index():
    return {"message": "hello to room reservations app"}

@action("register_room")
@action.uses("generic.html", auth.user)
def register_room():
    form = Form(db.room)  # Create Form
    if form.accepted:
        redirect(URL("list_rooms"))
    return locals()

@action("edit_room/<room_id:int>")
@action.uses("generic.html", auth.user)
def register_room(room_id):
    form = Form(db.room, room_id) # Update form 
    if form.accepted:
        redirect(URL("list_rooms"))
    return locals()

@action("list_rooms")
@action.uses("list_rooms.html", auth.user)
def list_rooms():
    rows = db(db.room).select() # Selecting rooms
    return locals()

@action("make_reservation/<room_id:int>")
@action.uses("make_reservation.html", auth.user)
def make_reservation(room_id):    
    error = ""
    form = Form([
        Field("start", "datetime", default="2025-06-10 12:00:00",requires=IS_DATETIME()),
        Field("end", "datetime", default="2025-06-10 12:00:00",requires=IS_DATETIME())])
    if form.accepted:
        start = form.vars["start"]
        end = form.vars["end"]
        minutes = (end - start).total_seconds()/60
        if minutes < 10 or minutes > 24*60:
            error = "reservation too short or too long"            
        elif db((db.reservation.start_datetime < end)&
                (db.reservation.stop_datetime > start)&
                (db.reservation.room_id==room_id)).count() > 0:
            error = "conflicting reservations"
        else:            
            ret = db.reservation.insert(
                user_id=auth.user_id,
                room_id=room_id,
                start_datetime=form.vars["start"],
                stop_datetime=form.vars["end"],
            )
            redirect(URL("list_my_reservations"))
    return locals()

@action("list_my_reservations")
@action.uses("list_my_reservations.html", auth.user)
def list_my_reservations():
    rows = db(
        (db.reservation.user_id==auth.user_id)&
        (db.reservation.start_datetime>datetime.datetime.now())
    ).select(orderby=db.reservation.start_datetime)
    return locals()

"""
old code
def make_reservation(room_id):    
    db.reservation.room_id.readable = False
    db.reservation.room_id.writable = False
    db.reservation.room_id.default = room_id
    db.reservation.user_id.readable = False
    db.reservation.user_id.writable = False
    db.reservation.user_id.default = auth.user_id
    db.reservation.start_datetime.default = "2025-06-10 12:00:00"
    db.reservation.stop_datetime.default = "2025-06-10 13:00:00"
    form = Form(db.reservation)
    if form.accepted:        
        redirect(URL("list_my_reservations"))
    return locals()
"""