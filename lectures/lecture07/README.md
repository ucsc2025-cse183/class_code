Python Frameworks:
- Django
- Flask
- Pylons
- Turbogears
- CherryPy
- web2py (2007)
- py4web

Ruby
- Ruby on rails



## references
https://bottlepy.org/docs/dev/api.html#bottle.request

### how to create an app

Option 1
mkdir apps/todo
# cp -r apps/_scaffold/* apps/todo
cp -r apps/_minimal/* apps/todo


Option 2
visit http://127.0.0.1:8000/_dashboard and press button [create app]


## Web framework features

- web server
- ability to serve static files
- routing: mapping URL into function call
- parsing of request
- session management (store transient information, in cookie, in database, other serverside storage)
- cache (store information shared often used)
- templating (generate HTML from a template)
- database abstraction layer or object relational mapper
- generate forms and tables and grid and othe thing
- internationalization (i18n) & pluralization
- database interface (_dashboard)
- error handing -> ticket + ticket interface (_dashboard)
- authentication
- authorization
- single sign on
- run backgroud tasks
- handle image and videos and streaming of video
- 