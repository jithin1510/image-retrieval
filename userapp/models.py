from contextlib import nullcontext
from msilib.schema import Class
from django.db import models
from dataownerapp.models import DataOwnerModel
from userapp.models import *

# Create your models here.
class UserModel(models.Model):
    user_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    mobile=models.BigIntegerField(null=True)
    location=models.CharField(max_length=100)
    pwd=models.CharField(max_length=100)
    cpwd=models.CharField(max_length=100)
    status=models.CharField(default='pending',null=True,max_length=100)

    class Meta():
        db_table='user_register'


class RequestModel(models.Model):
    request_id=models.AutoField(primary_key=True)
    user_id=models.BigIntegerField(null=True)
    owner_id=models.BigIntegerField(null=True)
    file_id=models.BigIntegerField(null=True)
    imagename=models.CharField(max_length=100,null=True)
    image=models.ImageField(upload_to='requests/',null=True)
    status=models.CharField(default='Pending',null=True,max_length=100)
    key=models.CharField(null=True,max_length=100)
    file_name = models.CharField(max_length=100,null=True)

    class Meta():
        db_table='request_model'