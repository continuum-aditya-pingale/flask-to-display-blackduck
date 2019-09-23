from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os

app = Flask(__name__)



@app.route("/showdata",methods=["GET"] )

def tasks ():
    
    name1=request.args.get('name')
    project_name=name1
    client = MongoClient() #host uri
    db = client.dashboarddb #Select the database
    #Select the collection name
    collection = db.blackduck
    result = collection.find()

    return render_template('index.html',name=name1, result = result, project_name = project_name)


if __name__ == "__main__":
    app.run()
