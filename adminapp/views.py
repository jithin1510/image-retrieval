from email import message
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from userapp.models import *
from dataownerapp.models import *





def admin_login(request):

    if request.method == "POST":
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')

        if name=='admin' and pwd=='admin':
            messages.success(request,'successfully logged-in')
            return redirect('admin-home')
        else:
            return redirect('admin-login')
    return render(request,'admin/admin-login.html')


def admin_home(request):

    users=UserModel.objects.all().count()
    data=DataOwnerModel.objects.all().count()
    upload=UploadModel.objects.all().count()
    requests=RequestModel.objects.all().count()

    req=RequestModel.objects.all()

    return render(request,'admin/admin-home.html',{'users':users,'data':data,'upload':upload, 'requests':requests,'req':req})


def admin_view_users(request):
    users=UserModel.objects.all().order_by('-user_id')
    return render(request,'admin/admin-view-users.html',{'users':users})


def admin_view_request(request):
    req=RequestModel.objects.all().order_by('-request_id')
    return render(request,'admin/admin-view-request.html',{'req':req})


def admin_view_dataowner(request):
    data=DataOwnerModel.objects.all().order_by('-dataowner_id')
    return render(request,'admin/admin-view-dataowner.html',{'data':data})


def accept_user(request,id):

    UserModel.objects.filter(user_id=id).update(status="Accepted")
    return redirect('admin-view-user')


def reject_user(request,id):
    UserModel.objects.filter(user_id=id).update(status="Rejected")
    return redirect('admin-view-user')


def accept_owner(request,id):

    DataOwnerModel.objects.filter(dataowner_id=id).update(status="Accepted")
    return redirect('admin-view-dataowner')



def reject_ownert(request,id):
    DataOwnerModel.objects.filter(dataowner_id=id).update(status="Rejected")
    return redirect('admin-view-dataowner')