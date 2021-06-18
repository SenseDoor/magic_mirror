#!/usr/bin/env python3
from bottle import get,post,run,request,template,route

@get("/")
def index():
    return template("index")
@post("/cmd")
def cmd():
    print("按下了按钮: "+request.body.read().decode())
    return "OK"

@route('/new',method='GET')
def memory():
    if request.GET.save:
        txt=request.GET.task.strip()
        print(txt)
    
    return template("index")


run(host="192.168.43.81",port=8080)
#<input type="text" size="50" maxlength="50" name="task">
