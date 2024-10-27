from django.http import HttpResponse
from django.shortcuts import render
import pymysql
import requests
mydb=pymysql.connect(host="localhost",user="root",password="root",database="maliciousurl")
def page1(request):
    return render(request,"page1.html")
def register(request):
    return render(request,"NewRegistration.html")
def login(request):
    name=request.POST.get('name')
    contact=request.POST.get('cnumber')
    email=request.POST.get('email')
    password=request.POST.get('pass')
    cur=mydb.cursor()
    sql="insert into user(name,contact,email,password)values(%s,%s,%s,%s)";
    values=(name,contact,email,password)
    cur.execute(sql,values)
    mydb.commit()
    return render(request,"NewRegistration.html")
def userlogin(request):
    sql="select * from user";
    cur1=mydb.cursor()
    cur1.execute(sql)
    data=cur1.fetchall()
    email=request.POST.get('email')
    password=request.POST.get('pass')
    #print(email)
    #print(password)
    uname="";
    uid="";
    ispresent=False
    
    if(email=="admin" and password=="admin"):
        return render(request,"AdminDashboard.html")
    else:
        for x in data:
            if(x[3]==email and x[4]==password):
                uname=x[1]
                uid=x[0]
                ispresent=True;
    if(ispresent):
        request.session['name']=uname
        request.session['uid']=uid
        return render(request,"UserDashboard.html")
    else:
        result="Invalid Username or Password"
        return render(request,"page1.html",{'data':result})
    print(ispresent)
