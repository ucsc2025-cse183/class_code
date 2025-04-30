# Satabase Abstraction Layer API

## import API

from py4web import DAL, Field
from pydal import DAL, Field

## Create a db connection

db = DAL("sqlite://storage.sqlite", folder="/tmp")

## define tables

db.define_table("dog", Field("name"), Field("color"))

## insert records

snoopy_id = db.dog.insert(name="Snoopy", color="white")

## retrieve individual record

row = db.dog[1]
db.dog[snoopy_id].name
db.dog[snoopy_id].delete_record()
db.dog[snoopy_id].update_record(name="Snoopy")

## select records

query = db.dog.name > "M"
queryset = db(query)
rows = queryset.select()
row = rows[0]

rows = db(db.dog.name > "M").select()
for row in rows: print(row.name, row.color)

## update records

db(db.dog.name > "M").update(color="brown")
db(db.dog.name > "M").delete()

db(db.dog.id == snoopy_id).delete()
db(db.dog.id == snoopy_id).update(name="Snoopy", color="white")

