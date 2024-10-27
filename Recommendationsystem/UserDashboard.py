from django.http import HttpResponse
from django.shortcuts import render
import pymysql
from datetime import date
import time
import json
import requests
import pandas as pd
import urllib.request
from datetime import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
mydb=pymysql.connect(host="localhost",user="root",password="root",database="maliciousurl")

def userdashboard(request):
    print("Username",request.session['username'])
    return render(request,"UserDashboard.html")

def userhome(request):
  
    #print("Username",request.session['username'])
    return render(request,"UserDashboard.html")
def addstopword(request):
    return render(request,"AddStopWord.html")
def logout(request):
    return render(request,"page1.html")
def insertstopword(request):
    title=request.POST.get('title')
    cur=mydb.cursor()
    sql="insert into stopword(stopword)values(%s)";
    values=(title)
    cur.execute(sql,values)
    mydb.commit()
    return render(request,"addstopword.html")
def extracturl(request):
    title=request.POST.get('title')
    context ={
    'news': title, 
    }
    return render(request,"ExtractedNews.html",context)
def applystopwordremovel(request):
    title=request.POST.get('title')
    req = Request(title, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    webpage = urlopen(req).read()
    parsed_html = BeautifulSoup(webpage)
    data=""
    for link in parsed_html.find_all('body'):
        data=data+link.text
        
    #print(title)
    x=data.split()
    afer_stopword=""
    cur=mydb.cursor()
    sql="select * from stopword";
    cur1=mydb.cursor()
    cur1.execute(sql)
    data=cur1.fetchall()
    worddata=""
    is_stop=False
    for word in x:
        is_stop=True
        print(word)
        for y in data:
            if(word.strip()==y[1].strip()):
                is_stop=False
                print(is_stop)
        if(is_stop):
            worddata=worddata+" "+word
    print("Data",worddata)
    context ={
    'filtered': worddata,
    'url':title
    }
    return render(request,"StopwordRemoval.html",context)

def predictedresult(request):
    Sexual=0
    Offensive=0
    Abusing=0
    Violant=0
    news = request.POST.get('title')
    #------------------filteration------------------------------
    title=request.POST.get('title')
    req = Request(title, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    parsed_html = BeautifulSoup(webpage)
    data=""
    for link in parsed_html.find_all('body'):
        data=data+link.text
        
    #print(title)
    x=data.split()
    afer_stopword=""
    cur=mydb.cursor()
    sql="select * from stopword";
    cur1=mydb.cursor()
    cur1.execute(sql)
    data=cur1.fetchall()
    worddata=""
    wordcount=0
    is_stop=False
    for word in x:
        wordcount=wordcount+1
        is_stop=True
        print(word)
        for y in data:
            if(word.strip()==y[1].strip()):
                is_stop=False
                print(is_stop)
        if(is_stop):
            worddata=worddata+" "+word
    x=worddata.split()
    
    cur=mydb.cursor()
    sql="select * from malword";
    cur1=mydb.cursor()
    cur1.execute(sql)
    data=cur1.fetchall()
    for word in x:
        for y in data:
            if(word.strip().lower()==y[1].strip().lower()):
                if(y[2]=='Sexual'):
                    Sexual=Sexual+1
                if(y[2]=='Offensive'):
                    Offensive=Offensive+1
                if(y[2]=='Abusing'):
                    Abusing=Abusing+1
                if(y[2]=='Violant'):
                    Violant=Violant+1    
           
    context ={
    'news' :news,
    'Sexual': Sexual,
    'Offensive'  :Offensive,
    'Abusing':Abusing,
    'Violant':Violant,
    'wordcount':wordcount,
    }
    return render(request,"PredictedResult.html",context)
def malicousdetection(request):
    url = request.POST.get('url')
    sexual = request.POST.get('sexual')
    Offensive=request.POST.get('sexual')
    Abusing=request.POST.get('Abusing')
    Violant=request.POST.get('Violant')
    wordcount=request.POST.get('wordcount')
    sex=int(sexual)
    off=int(Offensive)
    abu=int(Abusing)
    vio=int(Violant)
    wrd=int(wordcount)
    sex_ration=sex/wrd
    off_ration=off/wrd
    abu_ration=abu/wrd
    vio_ration=vio/wrd
    ismal="Malicious Url Not Found"
    total=(sex_ration*1000+off_ration*1000+abu_ration*1000+vio_ration*1000)
    if(total>0.5):
        ismal="Malicious Url Found"
    context ={
    'url' :url,
    'Sexual': sexual,
    'Offensive'  :Offensive,
    'Abusing':Abusing,
    'Violant':Violant,
    'wordcount':wordcount,
    'sex_ration':sex_ration,
    'off_ration':off_ration,
    'abu_ration':abu_ration,
    'vio_ration':vio_ration,
    'total':total,
    'ismal':ismal
    }
    #----------------updating db entry--------------------
    uname=request.session['name']
    uid=request.session['uid']
    cur1=mydb.cursor()
    #------------------Insertion----------------------
    sql="insert into results(uid,url,sexcount,offcount,violantcount,abucount,uname,malration,ismal)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values=(uid,url,sex_ration,off_ration,vio_ration,abu_ration,uname,total,ismal)
    cur1.execute(sql,values)
    mydb.commit()
    return render(request,"MaliciousDetection.html",context)


def insertcategorialword(request):
    title=request.POST.get('title')
    category=request.POST.get('category')
    cur=mydb.cursor()
    sql="insert into malword(word,category)values(%s,%s)";
    values=(title,category)
    cur.execute(sql,values)
    mydb.commit()
    return render(request,"AddCatWord.html")
def mysearches(request):
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
    return render(request,"MySearches.html", {'list': {'items':payload}})
def viewresults(request):
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
    return render(request,"MyResults.html", {'list': {'items':payload}})
def addcategorialword(request):
    return render(request,"AddCatWord.html")
def webcrawling(request):
    title=request.POST.get('title')
    #-------Session Extraction----------------------
    uname=request.session['name']
    uid=request.session['uid']
    cur1=mydb.cursor()
    today = datetime.now()
    #------------------Insertion
    sql="insert into usersearches(url,uid,uname,stime)values(%s,%s,%s,%s)"
    values=(title,uid,uname,today)
    cur1.execute(sql,values)
    mydb.commit()
    #----------------------
    lst={}
    lst["news"]=[]
    
    req = Request(title, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    webpage = urlopen(req).read()
    parsed_html = BeautifulSoup(webpage)
    for link in parsed_html.find_all('body'):
        lst["news"].append(link.text)
        #print(link.text,end="\n")
    df = pd.DataFrame(lst)
    #print(df)
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    #print(data)
    context = {'d': data,
               'url':title
               }
    return render(request,"WebCrawled.html",context)

def webcrawlinganalytics(request):
    lst={}
    lst["news"]=[]
    title=request.POST.get('title')
    req = Request('https://timesofindia.indiatimes.com/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    time.sleep(2)
    webpage = urlopen(req).read()
    parsed_html = BeautifulSoup(webpage)
    for link in parsed_html.find_all('a'):
        lst["news"].append(link.text)
        #print(link.text,end="\n")
    df = pd.DataFrame(lst)
    #print(df)
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    print(data)
    context = {'d': data}
    return render(request,"WebCrawled.html",context)
def viewdataset(request):
    sql="select * from datasets"
    #cur1=mydb.cursor()
    #cur1.execute(sql)
    
    list = [1,2,3,'String1']
    return render(request,"ViewDataset.html", {'list': list})
