from py4web import action, request
from .common import db, T
import time

@action("test")
@action.uses(db)
def index():
    key = request.query.key
    sql = f"SELECT * FROM thing WHERE (thing.name LIKE '%{key}%');"
    data = db.executesql(sql)
    # rows = db(db.thing.name.contains(key)).select()
    return f"<html><body><pre>{db._lastsql}</pre><pre>{data}</pre></body></html>"


@action("hello")
@action.uses(T)
def index():
    return str(T("Hello"))


@action("sleep")
def _():
    time.sleep(10)
    return "I woke up after 10 secons"

@action("quick")
def _():
    return f"I did not sleep {time.time()}"
