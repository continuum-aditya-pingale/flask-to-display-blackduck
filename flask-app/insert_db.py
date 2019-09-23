from pymongo import MongoClient 
  
try: 
    conn = MongoClient() 
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB") 
  
# database 
db = conn.dashboarddb
  
# Created or Switched to collection names: my_gfg_collection 
collection = db.blackduck
  
emp_rec1 = { 
        "version":"1634", 
        "SR":[{"H":0},{"M":2},{"L":4}],
        "OR":[{"H":0},{"M":2},{"L":4}],
        "LR":[{"H":0},{"M":2},{"L":4}]
        } 

  
# Insert Data 
rec_id1 = collection.insert_one(emp_rec1) 
 
  
print("Data inserted with record ids",rec_id1) 
