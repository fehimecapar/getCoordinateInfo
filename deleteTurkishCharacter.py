"""
mongodb'de tuttuğum veriler Türkçe karakterliydi bundan dolayı bul tarafında arama yaparken hata alıyordum Türkçe karakterleri
düzeltmek için unidecode kullandım. şu an da verilerim Türkçe karakterden arındırılmış bir şekilde gelmektedir.
"""
from unidecode import unidecode
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
db = client["sampledata"]
table = db["mahalleler"]

il_adi=""
ilce_adi=""
mahalle_adi=""
mahalle_id = 0
for x in table.find({}):
    for key, value in x.items():
        if key == "il_adi":
            il_adi=unidecode(value)
        elif key == "ilce_adi":
            ilce_adi=unidecode(value)
        elif key == "mahalle_adi":
            mahalle_adi = unidecode(value)
            if mahalle_adi:
                print("")
        elif key == "_id":
            mahalle_id = value

    # print("mahalle id: ", mahalle_id, "il adı: ", il_adi, "ilçe adı: ", ilce_adi, "mahalle_adi: ", mahalle_adi)
    # result = table.update_many(
    #
    #     {"_id": mahalle_id},
    #     {
    #         "$set": {
    #             "il_adi": il_adi,
    #             "ilce_adi": ilce_adi,
    #             "mahalle_adi": mahalle_adi},
    #         "$currentDate": {"lastModified": True}})








