from flask import Flask, request, redirect, render_template, session, url_for, jsonify, make_response, Response
# import json
# from flask_cors import CORS
import os
import string
import mysql.connector
from mysql.connector import Error

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Drum871225",
    database="website")

cursorTripData=mydb.cursor(buffered=True)
cursorTripData.execute("SELECT DATABASE();")	

app=Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)
app.config['JSON_AS_ASCII']=False
# app.config['JSONIFY_MIMETYPE'] ="charset=utf-8"
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["Access-Control-Allow-Origin"]="*"
app.config['CORS_HEADERS'] = 'Content-Type'

@app.before_request
def before_request():
    if request.path in ["", "/", "/api/attraction/<attractionId>", "/api/attractions", "/api/user", "/attraction/<id>", "/booking"] or "templates" in request.path:
        return None
    session.permanent=True
    user=session.get("status")

    # if user==False:
    #     return redirect("/")

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api/attraction/<attractionId>")
def apiAttraction(attractionId):
	sqlSearchResult={}
	cursorTripData.execute("SELECT _id, stitle, CAT2, xbody, address, info, MRT, latitude, longitude, images FROM TaipeiTripData where _id=%s;", (attractionId,))
	for (_id, stitle, CAT2, xbody, address, info, MRT, latitude, longitude, images) in cursorTripData: 
		sqlSearchResult={
			"data":{
				"id":_id,
				"name":stitle,
				"category":CAT2,
				"description":xbody,
				"address":address,
				"transport":info,
				"mrt":MRT,
				"latitude":latitude,
				"longitude":longitude,
				"images":images
			}
        }
	if cursorTripData.rowcount>0:
		pdimage=[]
		spImages=sqlSearchResult["data"]["images"].split('"')
		for spImage in spImages:
			img=str(spImage)
			if len(img) > 3:
				if img[-3]+img[-2]+img[-1] == "jpg":
					pdimage.append(img)
				if img[-3]+img[-2]+img[-1] == "JPG":
					pdimage.append(img)
				if img[-3]+img[-2]+img[-1] == "png":
					pdimage.append(img)
				if img[-3]+img[-2]+img[-1] == "PNG":
					pdimage.append(img)
		sqlSearchResult["data"]["images"]=pdimage
		return jsonify(sqlSearchResult)
	else:
		sqlSearchResult={
			"error":True,
			"message":"Attracions number error or does not exist."
		}
		return jsonify(sqlSearchResult), 400

@app.route("/api/attractions")
def apiAttractions():
	page=request.args.get("page", 0)
	page=int(page)
	keyword=request.args.get("keyword", "allAttractions")
	sqlSearchResult=[]
	if keyword == "allAttractions":
		cursorTripData.execute("SELECT _id, stitle, CAT2, xbody, address, info, MRT, latitude, longitude, images FROM TaipeiTripData LIMIT %s, %s;", (page*12,12))
		for (_id, stitle, CAT2, xbody, address, info, MRT, latitude, longitude, images) in cursorTripData: 
			attraction={
				"id":_id,
				"name":stitle,
				"category":CAT2,
				"description":xbody,
				"address":address,
				"transport":info,
				"mrt":MRT,
				"latitude":latitude,
				"longitude":longitude,
				"images":images
			}
			pdimage=[]
			spImages=attraction["images"].split('"')
			for spImage in spImages:
				img=str(spImage)
				if len(img) > 3:
					if img[-3]+img[-2]+img[-1] == "jpg":
						pdimage.append(img)
					if img[-3]+img[-2]+img[-1] == "JPG":
						pdimage.append(img)
					if img[-3]+img[-2]+img[-1] == "png":
						pdimage.append(img)
					if img[-3]+img[-2]+img[-1] == "PNG":
						pdimage.append(img)
			attraction["images"]=pdimage
			sqlSearchResult.append(attraction)
	else:
		cursorTripData.execute("SELECT _id, stitle, CAT2, xbody, address, info, MRT, latitude, longitude, images FROM TaipeiTripData where stitle LIKE %s LIMIT %s, %s;", ("%"+keyword+"%", page*12, 12))
		for (_id, stitle, CAT2, xbody, address, info, MRT, latitude, longitude, images) in cursorTripData: 
			attraction={
				"id":_id,
				"name":stitle,
				"category":CAT2,
				"description":xbody,
				"address":address,
				"transport":info,
				"mrt":MRT,
				"latitude":latitude,
				"longitude":longitude,
				"images":images
			}
			pdimage=[]
			spImages=attraction["images"].split('"')
			for spImage in spImages:
				img=str(spImage)
				if len(img) > 3:
					if img[-3]+img[-2]+img[-1] == "jpg":
						pdimage.append(img)
					if img[-3]+img[-2]+img[-1] == "JPG":
						pdimage.append(img)
					if img[-3]+img[-2]+img[-1] == "png":
						pdimage.append(img)
					if img[-3]+img[-2]+img[-1] == "PNG":
						pdimage.append(img)
			attraction["images"]=pdimage
			sqlSearchResult.append(attraction)
	apiAttractionsJson={"nextPage":page+1, "data":sqlSearchResult}
	if len(sqlSearchResult)==0:
		apiAttractionsJson={"nextPage":None, "data":None}
	# return json.dumps(apiAttractionsJson, ensure_ascii=False)
	return jsonify(apiAttractionsJson)

@app.route("/api/booking", methods=["GET", "POST", "DELETE"])
def apiBooking():
	replyMessage={}
	if request.method == "POST":
		inquireAttraction=request.get_json()
		if inquireAttraction["attraction"] != "" and inquireAttraction["date"] != "" and inquireAttraction["price"] != "":
			sqlSearchResult={}
			cursorTripData.execute("SELECT _id, stitle, address, images FROM TaipeiTripData where _id=%s;", (inquireAttraction["attraction"],))
			for (_id, stitle, address, images) in cursorTripData: 
				sqlSearchResult={
					"id":_id,
					"name":stitle,
					"address":address,
					"image":images
				}
			pdimage=[]
			spImages=sqlSearchResult["image"].split('"')
			for spImage in spImages:
				img=str(spImage)
				if len(img) > 3:
					if img[-3]+img[-2]+img[-1] == "jpg":
						pdimage.append(img)
					if img[-3]+img[-2]+img[-1] == "JPG":
						pdimage.append(img)
					if img[-3]+img[-2]+img[-1] == "png":
						pdimage.append(img)
					if img[-3]+img[-2]+img[-1] == "PNG":
						pdimage.append(img)
			sqlSearchResult["image"]=pdimage[0]
			inquireAttraction["attraction"]=sqlSearchResult
			session["spotScheduled"].append(inquireAttraction)
			replyMessage["ok"]=True
			return jsonify(replyMessage), 200
		elif inquireAttraction["attraction"] == "" or inquireAttraction["date"] == "":
			replyMessage["error"]=True
			replyMessage["message"]="格式錯誤或未填寫完成"
			print("Sorry")
			return jsonify(replyMessage), 400
		else:
			replyMessage["error"]=True
			replyMessage["message"]="未登入系統"
			return jsonify(replyMessage), 403
	if request.method == "GET":
		username=session.get("username")
		print(session["spotScheduled"])
		return jsonify(session["spotScheduled"]), 200
	if request.method == "DELETE":
		replyMessage["ok"]=True
		session["spotScheduled"]=[]
		return jsonify(replyMessage), 200

@app.route("/api/user", methods=["GET", "POST", "PATCH", "DELETE"])
def apiUser():
	sqlSearchResult={}
	replyMessage={}
	if request.method == "GET":
		cursorTripData.execute("select name, email, password from user where email=%s;", (session.get("status"),))
		for (name, email, password) in cursorTripData:
			sqlSearchResult={
				"data":{
					"name":name,
					"email":email,
					"password":password
				}
			}
		print(sqlSearchResult)
		userStatus=session.get("status")
		if userStatus == False:
			sqlSearchResult={}
			return jsonify(sqlSearchResult)
		return jsonify(sqlSearchResult)
	if request.method == "POST":
		inquireUserData=request.get_json()
		print(inquireUserData)
		cursorTripData.execute("select name, email, password from user where email=%s;", (inquireUserData["registerEmail"],))
		for (name, email, password) in cursorTripData:
			sqlSearchResult={
				"name":name,
				"email":email,
				"password":password
			}
		if cursorTripData.rowcount<=0 and inquireUserData["registerName"] != "" and inquireUserData["registerEmail"] != "" and inquireUserData["registerPassword"] != "":
			sql='INSERT INTO user (name, email, password) VALUES (%s, %s, %s);'
			newUser=(inquireUserData["registerName"], inquireUserData["registerEmail"], inquireUserData["registerPassword"])
			cursor=mydb.cursor()
			cursor.execute(sql, newUser)
			mydb.commit()
			replyMessage["ok"]=True
			return jsonify(replyMessage), 200
		else:
			replyMessage["error"]=True
			replyMessage["message"]="註冊失敗，重複的 Email 或其他原因"
			print(replyMessage)
			return jsonify(replyMessage), 400
	if request.method == "PATCH":
		inquireUserData=request.get_json()
		cursorTripData.execute("select name, email, password from user where email=%s;", (inquireUserData["signInEmail"],))
		for (name, email, password) in cursorTripData:
			sqlSearchResult={
				"name":name,
				"email":email,
				"password":password
			}
		if cursorTripData.rowcount>0:
			if sqlSearchResult["email"]==inquireUserData["signInEmail"] and sqlSearchResult["password"]==inquireUserData["signInPassword"]:
				session["username"]=sqlSearchResult["name"]
				session["status"]=sqlSearchResult["email"]
				session["spotScheduled"]=[]
				replyMessage["ok"]=True
				return jsonify(replyMessage), 200
			else:
				replyMessage["error"]=True
				replyMessage["message"]="格式錯誤或信箱已被註冊"
				return jsonify(replyMessage), 400
		else:
			replyMessage["error"]=True
			replyMessage["message"]="格式錯誤或信箱已被註冊"
			return jsonify(replyMessage), 400
	if request.method == "DELETE":
		print(str(session["status"])+", Logged Out")
		session["status"]=False
		session["spotScheduled"]=False
		replyMessage["ok"]=True
		return jsonify(replyMessage), 200

@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")
	
@app.errorhandler(500)
def internal_error(error):
	sqlSearchResult={
		"error":True,
		"message":"Error"
	}
	return json.dumps(sqlSearchResult), 500

app.run(host="0.0.0.0", port=3000, debug=True)