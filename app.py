from flask import Flask, request, redirect, render_template, session, url_for, jsonify, make_response, Response
# import json
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
app.config['JSON_AS_ASCII']=False
# app.config['JSONIFY_MIMETYPE'] ="charset=utf-8"
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["Access-Control-Allow-Origin"]="*"
app.config['CORS_HEADERS'] = 'Content-Type'

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

@app.route("/api/attractions", methods=["POST", "GET"])
def apiAttractions():
	page=request.args.get("page", 0)
	page=int(page)
	searchKeyword=request.get_json()
	keyword=request.args.get("keyword", "allAttractions")
	sqlSearchResult=[]
	if searchKeyword == None:
		sqlSearchResult=[]
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
			apiAttractionsJson={"nextPage":page+1, "data":sqlSearchResult}
		apiAttractionsJson={"nextPage":page+1, "data":sqlSearchResult}
		if len(sqlSearchResult)==0:
			apiAttractionsJson={"nextPage":None, "data":None}
		return make_response(jsonify(apiAttractionsJson), 200)
	else:
		cursorTripData.execute("SELECT _id, stitle, CAT2, xbody, address, info, MRT, latitude, longitude, images FROM TaipeiTripData where stitle LIKE %s LIMIT %s, %s;", ("%"+searchKeyword["searchKeyword"]+"%", page*12, 12))
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
			return make_response(jsonify(apiAttractionsJson), 200)
		print(sqlSearchResult)
		return make_response(jsonify(apiAttractionsJson), 200)

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