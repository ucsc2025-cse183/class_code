# Model View Controller

https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller

## Model

Part of the code that describes how data is stored.
white tables and which columns you want and their relations.

Database Abstraction Layer or Object Relational Mapper
SQLAlchemy

## View or template

Part of the code that descibes how data is to be represented to the user.

## Controller

Part of the code in charge of the business logic. Workflow.

## Static files

Files that need no processing

## Routing

@action("path")
def myfunction(): return "hello"

## py4web Keywords

from py4web import action, request, response, redirect, HTTP, URL, DAL, Field
from .common import db, session, Auth, cache, T

### Getting variables from request

GET ?a=1 => request.query.a
POST a=1 => request.POST.a
request.vars.a

