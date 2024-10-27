from django.http import HttpResponse
from django.shortcuts import render
import pymysql
from datetime import date
import json
import requests
import pandas as pd
import urllib.request
from datetime import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
mydb=pymysql.connect(host="localhost",user="root",password="root",database="maliciousurl")

def allsearches(request):
    sql="select * from usersearches";
    cur1=mydb.cursor()
    cur1.execute(sql)
    result=cur1.fetchall()
    payload = []
    content={}
    #json=jsonify(result)
    for row in result:
        content = {'url': row[1], 'stime': row[4]}
        payload.append(content)
        content = {}
    print(f"json: {json.dumps(payload)}")
    return render(request,"AllSearches.html", {'list': {'items':payload}})
def allresults(request):
    sql="select * from results";
    cur1=mydb.cursor()
    cur1.execute(sql)
    result=cur1.fetchall()
    payload = []
    content={}
    #json=jsonify(result)
    for row in result:
        content = {'url': row[2], 'sexcount': row[3],'offcount': row[4],'viocount': row[5],'abucount': row[10],'ismal': row[11]}
        payload.append(content)
        content = {}
    print(f"json: {json.dumps(payload)}")
    return render(request,"AllResults.html", {'list': {'items':payload}})
