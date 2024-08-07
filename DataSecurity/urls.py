"""DataSecurity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
import imp
from xml.dom.minidom import Document
from django.conf import settings
from django.contrib import admin
from django.urls import path
from userapp import views as user_views
from adminapp import views as admin_views
from mainapp import views as main_views
from dataownerapp import views as dataowner_views
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),

    # main app
    path('',main_views.index,name='index-page'),

    # admin app
    path('admin-login',admin_views.admin_login,name='admin-login'),
    path('admin-home',admin_views.admin_home,name='admin-home'),
    path('admin-view-user',admin_views.admin_view_users,name='admin-view-user'),
    path('admin-view-dataowner',admin_views.admin_view_dataowner,name='admin-view-dataowner'),
    path('admin-view-request',admin_views.admin_view_request,name='admin-view-request'),
    path('accept-user/<int:id>/',admin_views.accept_user,name='accept-user'),
    path('reject-user/<int:id>/',admin_views.reject_user,name='reject-user'),
    path('accept-owner/<int:id>/',admin_views.accept_owner,name='accept-owner'),
    path('accept-owner/<int:id>/',admin_views.accept_owner,name='accept-owner'),


    # user app
    path('user-register',user_views.user_register,name='user-register'),
    path('user-login',user_views.user_login,name='user-login'),
    path('user-home',user_views.user_home,name='user-home'),
    path('user-view-image',user_views.user_view_images,name='user-view-image'),
    path('user-view-status',user_views.user_status,name='user-view-status'),
    # path('user-status/<int:id>/',user_views.user_status,name='user-status'),
    path('user-profile',user_views.user_profile,name='user-profile'),
    path('request-download/<int:id>/',user_views.request_download,name='request-download'),
    path('verify-file/<int:id>/',user_views.verify_file,name='verify-file'),
    path('download-file/<int:id>/',user_views.download_file,name='download-file'),


    # dataowner app
    path('dataowner-register',dataowner_views.dataowner_register,name='dataowner-register'),
    path('dataowner-login',dataowner_views.dataowner_login,name='dataowner-login'),
    path('dataowner-home',dataowner_views.dataowner_home,name='dataowner-home'),
    path('dataowner-request',dataowner_views.dataowner_request,name='dataowner-view-request'),
    path('dataowner-profile',dataowner_views.dataowner_profile,name='dataowner-profile'),
    path('dataowner-upload',dataowner_views.dataowner_upload,name='dataowner-upload'),
    path('dataowner-view-upload',dataowner_views.dataowner_view_upload,name='dataowner-view-upload'),
    path('accept-generate-key/<int:id>/',dataowner_views.accept_generate_key,name='accept-generate-key'),
    path('reject-download/<int:id>/',dataowner_views.reject_download,name='reject-download'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
