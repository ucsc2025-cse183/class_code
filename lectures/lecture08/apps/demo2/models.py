from py4web import DAL, Field


db = DAL("sqlite://mystorage.sqlite")
# db = DAL("postgresql://....")
# db = DAL("oracle://....")

db.define_table(
    "color",
    Field("name"),
    Field("image", "upload")
)

if db(db.color).count() == 0:
    db.color.insert(name="green")
    db.color.insert(name="red")    
    db.color.insert(name="blue")    
    db.color.insert(name="purple")
    print(db(db.color).select())
    db.commit()
