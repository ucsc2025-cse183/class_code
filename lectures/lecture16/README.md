# Server Side Web Frameworks (py4web)

## Routing (map URL -> function call)

@action("a/b/c/index")
def myfunction(): return "hello world"

## Parsing of request

request.path
request.query
request.json
request.POST

## handles REST requests (filter by HTTP Method GET/POST/PUT/DELETE)

@action("a/b/c/index", method="GET")
def myfunction(): return {} # automatically converts output to JSON

## Session management

@action("a/b/c/index", method="GET")
@action.uses(session)
def myfunction(): 
    if "x" in session:
       session.x += 1
    else:
       session.x = 1
    return f"my counter is {session.x}"

## Templating: convert output to HTML or other text format

@action("a/b/c/index", method="GET")
@action.uses("index.html")
def myfunction():
    return {x: 2}

assuming "index.html" contains "...[[=x]]...[[for i in range(x):]]...[[pass]]"

## Caching (think of Kafka)

@action('hello/<name>')
@cache.memoize(expiration=60)
def hello(name):    
    return "Hello %s your code is %s" % (name, uuid.uuid4())

## Handle Database Abstraction

Pros:
- builds SQL for you in database agnostic manner
- prevents SQL injections
- parses data from db

## Handles Authentication

- provide login/logout/register/change password
- recognize users throught session

## Handle Authorization

- check if user is authorized to perform an action
- for exmaple check if user is logged in

@action.uses(auth.user)

## Form generation and processing (CRUD)

@action('index')
@action.uses(db)
def index():    
    form = Form(db.thing)  # create form
    return locals()

@action('index')
@action.uses(db)
def index():    
    form = Form(db.thing, 3, readonly=True)
    return locals()

@action('index')
@action.uses(db)
def index():    
    form = Form(db.thing, 3, deletable=True)  # update form
    return locals()

## Ability to stream output

## Internationalization (i18n)

T("Hello") will read translation into language.json

n_things = db(db.thing).count()
return T("I found {n} things", n=n_things)

n==0 => "Non ho trovato"
n==1 => "Ho trovato ona cosa"
n==2 => "Ho trovato 2 cose"

## _dashboard (unique of py4web)

## ability to host multiple apps (specific of py4web)

## cuncerrency

Ability to handle multiple requests at the same time without blocking other requests
each request has its own database connection and database session

## HTTPS and certificates

### Things left to do

- fix T!
- handling of images and videos
- security
- deployments with certificates





