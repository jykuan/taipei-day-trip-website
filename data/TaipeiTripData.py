import json
import mysql.connector
from mysql.connector import Error

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Drum871225",
    database="website")

cursorTripData=mydb.cursor(buffered=True)
cursorTripData.execute("SELECT DATABASE();")

with open("taipei-attractions.json", mode="r", encoding="utf-8") as file:
    data=json.load(file)

for tripData in data["result"]["results"]:

    # tripData["images"] 處理
    images=[]
    pdimage=[]
    images.append(tripData["file"])
    spImages=images[0].split("http://")
    for image in spImages:
        img="http://"+image
        if img[-3]+img[-2]+img[-1] == "jpg":
            pdimage.append(img)
        if img[-3]+img[-2]+img[-1] == "JPG":
            pdimage.append(img)
        if img[-3]+img[-2]+img[-1] == "png":
            pdimage.append(img)
        if img[-3]+img[-2]+img[-1] == "PNG":
            pdimage.append(img)

    pdXpostDate=tripData["xpostDate"][0:4]+"-"+tripData["xpostDate"][5:7]+"-"+tripData["xpostDate"][8:10]
    pdAvBegin=tripData["avBegin"][0:4]+"-"+tripData["avBegin"][5:7]+"-"+tripData["avBegin"][8:10]
    pdAvEnd=tripData["avEnd"][0:4]+"-"+tripData["avEnd"][5:7]+"-"+tripData["avEnd"][8:10]

    sql='INSERT INTO TaipeiTripData (info, stitle, xpostDate, longitude, REF_WP, avBegin, langinfo, MRT, SERIAL_NO, RowNumber, CAT1, CAT2, MEMO_TIME, POI, images, idpt, latitude, xbody, _id, avEnd, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
    newresult=(tripData["info"], tripData["stitle"], pdXpostDate, tripData["longitude"], tripData["REF_WP"], pdAvBegin, tripData["langinfo"], tripData["MRT"], tripData["SERIAL_NO"], tripData["RowNumber"], tripData["CAT1"], tripData["CAT2"], tripData["MEMO_TIME"], tripData["POI"], json.dumps(pdimage), tripData["idpt"], tripData["latitude"], tripData["xbody"], tripData["_id"], pdAvEnd, tripData["address"])
    cursor = mydb.cursor()
    cursor.execute(sql, newresult)
    mydb.commit()