from pymongo import MongoClient
import requests
import json
client = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")

db = client["sampledata"]
mahalleTable = db["mahalleler"]
latlngTable = db["latlng_mahalleler"]

temp_mahalle_adi = ''
mahalle_id = 0
var_mi = 0
idIsFound = False # tablo tarama işleminden sonra en son eklenen verinin id'sini yakalamak için tanımlanmıştır

for x in mahalleTable.find({}):
    query_string = ''
    for key, value in x.items():
        if key == "il_adi":
            il_adi=value
            query_string += value + ', '
        elif key == "ilce_adi":
            query_string += value + ', '
            ilce_adi = value
        elif key == "mahalle_adi":
            mahalle_adi = value
            if value == temp_mahalle_adi:
                query_string = ''
                break
            temp_mahalle_adi = value
            query_string += value
        elif key == "_id":
            mahalle_id = value
            if value == 87201 and idIsFound == False:
                idIsFound = True

    if query_string != '' and idIsFound == True:
        print(query_string)
        url = "https://pro.atlas.gov.tr/geo.sys?https%3A%2F%2Fmaps.googleapis.com%2Fmaps%2Fapi%2Fplace%2Ffindplacefromtext%2Fjson%3Finput=" + query_string + "&language=tr-TR&inputtype=textquery&fields=icon%2Cphotos%2Cformatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key=AIzaSyD1XHMDGP8AGuVeCAaE7NCnEMfjOYLsvvg"
        r = requests.get(url)
        if(r):
            print(r.content)
            y = json.loads(r.content)
            print(y)
            if 'candidates' in y and y['candidates'] != []: #{'ContentEncoding': None, 'ContentType': None, 'Data': {'Error': None, 'ErrorObjs': [], 'Success': None, 'SuccessObjs': [], 'SuccessLogIdList': [], 'ErrorLogIdList': [], 'TotalCount': 0, 'CallStart': '0001-01-01T00:00:00', 'CallEnd': '0001-01-01T00:00:00', 'SessionStartTime': None, 'AllowedToReadColumnNameList': None, 'AllowedToWriteColumnNameList': None}, 'JsonRequestBehavior': 0, 'MaxJsonLength': 2147483647, 'RecursionLimit': None}

                z = json.loads(json.dumps(y['candidates']))
                #print("mahalle_id",mahalle_id)
                if'geometry' in z[0]:
                    b = json.loads(json.dumps(z[0]['geometry']))
                    if 'location' in b:
                        location = json.loads(json.dumps(b['location']))
                        #print(location)
                        lat = location['lat']
                        lng = location['lng']
                        #print("lat",lat , "\nlng",lng)
                        #print(mahalle_id)
                        db.get_collection('latlng_mahalleler').insert_one({"_id":mahalle_id ,"data":{"lat":lat, "lng":lng}})

