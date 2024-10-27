"""Recommendationsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import index
from . import UploadDataset
from . import UserDashboard
from . import AdminDashboard
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', index.page1),
    path('admin/', admin.site.urls),
    path('page1',index.page1),
    path('register',index.register),
    path('login',index.login),
    path('userlogin',index.userlogin),
    path('uploaddataset',UploadDataset.upload2),
    path('adminhome',UploadDataset.adminhome),
    path('uploaddataset1',UploadDataset.uploaddataset),
    path('viewdataset',UploadDataset.viewdataset),
    path('logout',UploadDataset.logout),
    path('viewuser',UploadDataset.viewuser),
    path('addstopword',UserDashboard.addstopword),
    path('insertstopword',UserDashboard.insertstopword),
    path('userhome',UserDashboard.userhome),
    path('addcategorialword',UserDashboard.addcategorialword),
    path('userhome',UserDashboard.userdashboard),
    path('userdashboard',UserDashboard.userdashboard),
    path('insertcategorialword',UserDashboard.insertcategorialword),
    path('extracturl',UserDashboard.extracturl),
    path('viewresults',UserDashboard.viewresults),  
    path('predictedresult',UserDashboard.predictedresult),
    path('mysearches',UserDashboard.mysearches),
    path('applystopwordremovel',UserDashboard.applystopwordremovel),   
    path('webcrawling',UserDashboard.webcrawling),
    path('webcrawling',UserDashboard.webcrawlinganalytics),  
    path('malicousdetection',UserDashboard.malicousdetection),
    path('allsearches',AdminDashboard.allsearches),
    path('allresults',AdminDashboard.allresults),
    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
