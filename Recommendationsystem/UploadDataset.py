from django.http import HttpResponse
from django.shortcuts import render
from flask import jsonify
# Its good practice to have imports at the top of script.
import requests
import json
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
# We will create an object and store data from alpha vantage inside this object
from collections import namedtuple 
import json
import pymysql
mydb=pymysql.connect(host="localhost",user="root",password="root",database="maliciousurl")
def upload2(request):
    btn=request.POST.get('b1')
    print(btn)
    if(btn=="UploadDataset"):
        return render(request,"UploadDataset.html")
    if(btn=="ViewDataset"):
        return render(request,"ViewDataset.html")
    if(btn=="CleanDataset"):
        return render(request,"CleanDataset.html")

def adminhome(request):
    return render(request,"AdminDashboard.html")
def uploaddataset(request):
    return render(request,"UploadDataset.html")
def logout(request):
    return render(request,"page1.html")
def UploadEntry(request):
    title=request.POST.get('title')
    category=request.POST.get('category')
    file=request.POST.get('file')
    cur=mydb.cursor()
    sql="insert into datasets(DatasetTitke,Category,filepath)values(%s,%s,%s)";
    values=(title,category,file)
    cur.execute(sql,values)
    mydb.commit()
    return render(request,"UploadDataset.html")
class create_dict(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value
def viewdataset(request):
    sql="select * from datasets";
    cur1=mydb.cursor()
    cur1.execute(sql)
    result=cur1.fetchall()
    payload = []
    content={}
    mydict = create_dict()
    #json=jsonify(result)
    for row in result:
        content = {'title': row[1], 'category': row[2], 'filepath': row[3]}
        payload.append(content)
        content = {}
    print(f"json: {json.dumps(payload)}")
    return render(request,"ViewDataset.html", {'list': {'items':payload}})
    
def viewuser(request):
    sql="select * from user";
    cur1=mydb.cursor()
    cur1.execute(sql)
    result=cur1.fetchall()
    payload = []
    content={}
    mydict = create_dict()
    #json=jsonify(result)
    for row in result:
        content = {'name': row[1], 'contact': row[2], 'email': row[3]}
        payload.append(content)
        content = {}
    print(f"json: {json.dumps(payload)}")
    return render(request,"ViewUser.html", {'list': {'items':payload}})   
    
    
