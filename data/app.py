from flask import Flask, request, redirect, render_template, session, url_for, jsonify, make_response
# from datetime import datetime
from flask_cors import CORS
import os
import string
import mysql.connector
from mysql.connector import Error

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Drum871225",
    database="website")

cursorSignin = mydb.cursor(buffered=True)
cursorSignin.execute("SELECT DATABASE();")
app=Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)
app.config["JSON_AS_ASCII"] = False

@app.before_request
def before_request():
    if request.path in ["", "/", "/signin", "/error", "/signout", "/register", "/signup"] or "templates" in request.path:
        return None
    session.permanent=True
    user=session.get("status")

    if user==False:
        return redirect("/")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin", methods=["POST"])
def login():
    sqlSearchResult=[]
    requestAccount=request.form["account"]
    requestPassword=request.form["password"]
    cursorSignin.execute("select name, username, password from user where username=%s;", (requestAccount,))
    for (name, username, password) in cursorSignin:
        sqlSearchResult.append({
            "name":name,
            "username":username,
            "password":password
        })
    if cursorSignin.rowcount>0:
        if sqlSearchResult[0]["username"]==requestAccount and sqlSearchResult[0]["password"]==requestPassword:
            session["status"]=sqlSearchResult[0]["name"]
            memberName=sqlSearchResult[0]["name"]
            return redirect("http://127.0.0.1:3000/member")
        else:
            return redirect(url_for("error", message="帳號或密碼輸入錯誤"))
    else:
        return redirect(url_for("error", message="帳號或密碼輸入錯誤"))

@app.route("/register")
def register():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    sqlSearchResult=[]
    requestAccount=request.form["username"]
    global cur
    cursorSignin.execute("select username from user where username=%s;", (requestAccount,))
    for username in cursorSignin:
        sqlSearchResult.append({
            "username":username
        })
    if cursorSignin.rowcount<=0:
        sql='INSERT INTO user (name, username, password) VALUES (%s, %s, %s);'
        newuser=(request.form["name"], request.form["username"], request.form["password"])
        cursor = mydb.cursor()
        cursor.execute(sql, newuser)
        mydb.commit()
        return render_template("index.html")
    else:
        return redirect(url_for("error", message="帳號已經被註冊"))

@app.route("/member", methods=["POST", "GET"])
def member():
    memberName=session.get("status")
    nullName={"username":""}
    nullSession=nullName["username"]
    if memberName!=nullSession:
        print(str(session["status"])+", Logged In")
        return render_template("member.html", name=memberName)
    else:
        return redirect(url_for("error", message="帳號或密碼輸入錯誤"))

@app.route("/inquireusername", methods=["POST", "GET"])
def inquireusername():
    inquireUsername=request.get_json()
    sqlSearchResult=[]
    cursorSignin.execute("select name, username from user where username=%s;", (inquireUsername["username"],))
    for (name, username) in cursorSignin:
        sqlSearchResult.append({
            "name":name,
            "username":username
        })
    if cursorSignin.rowcount>0:
        inquireUsername["name"]=sqlSearchResult[0]["name"]
    else:
        inquireUsername["name"]="Sorry, there is no user."

    res=make_response(jsonify(inquireUsername), 200)
    return res

@app.route("/api/user", methods=["POST", "GET"])
def apiuser():
    updateName=request.get_json()
    nullStatus={"nullStatus":""}
    if updateName["name"] != nullStatus["nullStatus"]:
        sqlSearchResult=[]
        cursorSignin.execute("select name, username from user where name=%s;", (session["status"],))
        for (name, username) in cursorSignin:
            sqlSearchResult.append({
                "name":name,
                "username":username
            })
        cursorSignin.execute("update user set name = %s WHERE username = %s;", (updateName["name"], sqlSearchResult[0]["username"]))
        mydb.commit()
        session["status"]=updateName["name"]
        updateName["ok"]="true"
        res=make_response(jsonify(updateName), 200)
        return res
    else:
        updateName["error"]="true"
        res=make_response(jsonify(updateName), 200)
        return res

@app.route("/api/users")
def apiusers():
    inquireUser=request.args.get("username")
    sqlSearchResult=[]
    cursorSignin.execute("select id, name, username from user where username=%s;", (inquireUser,))
    for (id, name, username) in cursorSignin:
        sqlSearchResult.append({
            "id":id,
            "name":name,
            "username":username
        })
    if cursorSignin.rowcount>0:
        inquireData={"data":sqlSearchResult[0]}
        return inquireData
    else:
        inquireData={"data":"null"}
        return inquireData

@app.route("/error")
def error():
    errorMessage=request.args.get("message")
    return render_template("error.html", errorMessage=errorMessage)

@app.route("/signout")
def signout():
    print(str(session["status"])+", Logged Out")
    session["status"]=False
    return redirect("http://127.0.0.1:3000/")

app.run(port=3000, debug=True)