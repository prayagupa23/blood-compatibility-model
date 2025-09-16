import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb+srv://igniteIt:l6KeRHXcfFvXhiEy@blood-donation-cluster.ysphuoa.mongodb.net/?retryWrites=true&w=majority&appName=blood-donation-cluster")
db = client["test"]
collection = db["users"]

csv_file = "DONOR_DATA1.csv"

def append_to_csv(docs, filename = csv_file):
    docs.pop("_id",None)
    #donorList = list(docs)
    dataFrame = pd.json_normalize([docs])
    try:
        dataFrame.to_csv(csv_file, header=False ,mode='a',index=False) # ye existing csv file me data append karega and columns nahi banayega(header)
    except FileNotFoundError:
        dataFrame.to_csv(csv_file, mode='w', header=True, index=False) # ye file not found exception hua toh means file doesn't exist, so wo write karega ek new file me with header

pipeline = [
    {"$match" : {"operationType" : "insert" , "fullDocument.userType" : "donor" }}
]

with collection.watch(pipeline) as streams:
    for change in streams:
        doc = change["fullDocument"]
        append_to_csv(doc)

# query = {"userType" : "donor"}
# results = collection.find(query)


# donorList = list(results)

# if donorList:
#     dataFrame = pd.json_normalize(donorList)

#     if "_id" in dataFrame.columns:
#         dataFrame = dataFrame.drop(columns=["_id"])
#     #print(donorList)
#     dataFrame.to_csv('DONOR_DATA1.csv', index=False)
#     print("hogya bhai insert excel me")
# else:
#     print("nahi ho paya bhai sorry")