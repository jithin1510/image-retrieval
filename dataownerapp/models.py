from django.db import models


# Create your models here.
class DataOwnerModel(models.Model):
    dataowner_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    mobile=models.BigIntegerField()
    location=models.CharField(max_length=100)
    pwd=models.CharField(max_length=100)
    cpwd=models.CharField(max_length=100)
    status=models.CharField(default='pending',null=True,max_length=100)

    class Meta():
        db_table='dataowner_register'


class UploadModel(models.Model):
    id=models.AutoField(primary_key=True)
    file_id=models.BigIntegerField()
    dataowner_id=models.ForeignKey(DataOwnerModel,db_column='dataowner_id',on_delete=models.CASCADE,null=True,blank=True)
    imagename=models.CharField(max_length=100, null=True)
    image=models.ImageField(upload_to='images/',null=True)
    tags=models.CharField(max_length=100)
    encrpyt_key=models.TextField(max_length=500,null=True)
    file_name=models.CharField(max_length=100,null=True)
    enc_status = models.CharField(max_length=50,default='Encrypted')
    image_block = models.CharField(max_length=100,null=True)
    file_name_block = models.CharField(max_length=100,null=True)
    imagename_block = models.CharField(max_length=100,null=True)

    class Meta():
        db_table='owner_uploads'