from py4web import action, redirect, HTTP, response, request, URL


@action("test1")
@action.uses("mytemplate.html")
def test1():    
    hello = 1
    b = 2
    c = 3
    return {"a": hello, "b": b, "c":c}


@action("test2")
def test2():
    if request.method == "POST":
        if request.POST.a:
            return "form accepted!"
            # redirect(URL("test3"))
    return "<html><body><form method='POST' action='#'><input name='a'/></form></body></html>" # postback


@action("test3")
def test3():
    return "your form was processed!"

