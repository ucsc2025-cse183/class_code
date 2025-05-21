from py4web import action, redirect, URL, request
from . common import db

@action("index")
def index():
    redirect(URL("static", "index.html"))


#create a POST endpoint `api/birds` to register a new bird as required by index.js (1 point)
@action("api/birds", method="POST")
@action.uses(db)
def _():
    # received something like {'id': 0, 'name': 'penguin', 'habitat': '', 'weight': 0, 'sightings': 0}
    req = request.json
    if "id" in req:
        del req["id"]
    return db.bird.validate_and_insert(**req)

#create a GET endpoint `api/birds` to get birds as required by index.js (1 point)
@action("api/birds", method="GET")
@action.uses(db)
def _():
    return {"birds": db(db.bird).select().as_list()}

#create a POST endpoint `api/birds/{id}/increase_sightings` to increase the number of sightings by 1 (no body in POST) as required by index.js (1 point)
@action("api/birds/<bird_id:int>/increase_sightings", method="POST")
@action.uses(db)
def _(bird_id):
    bird = db.bird[bird_id]
    bird.update_record(sightings = bird.sightings + 1)
    return locals()

#create a PUT endpoint `api/birds/{id}` to update bird info as required by index.js (1 point)
@action("api/birds/<bird_id:int>", method="PUT")
@action.uses(db)
def _(bird_id):
    return db.bird.validate_and_update(bird_id, **request.json)

#create a DELETE endpoint `api/birds/{id}` to delete a bird (1 point)
@action("api/birds/<bird_id:int>", method="DELETE")
@action.uses(db)
def _(bird_id):
    bird = db.bird[bird_id]
    bird.delete_record()
    return locals()
