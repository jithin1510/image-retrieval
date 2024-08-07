import os
import random
import string
from hashlib import md5

from Crypto.Cipher import DES3
from cryptography.fernet import Fernet
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render

from dataownerapp.models import *
from DataSecurity.settings import DEFAULT_FROM_EMAIL
from userapp.models import RequestModel, UserModel
from DataSecurity.BlockcahinAlgo import HashDataBlock

# Create your views here.

def dataowner_register(request):

    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        print(mobile)
        location=request.POST.get('location')
        pwd=request.POST.get('pwd')
        cpwd=request.POST.get('cpwd')

        if DataOwnerModel.objects.filter(email=email):
            messages.warning(request,'Email Already Exists')
        else:
            DataOwnerModel.objects.create(name=name,email=email,mobile=mobile,location=location,pwd=pwd,cpwd=cpwd)
            messages.info(request,'Account Created')
            return redirect('dataowner-login')

    return render(request,'main/dataowner-register.html')


def dataowner_login(request):

    if request.method == "POST":
        email=request.POST.get('email')
        pwd=request.POST.get('pwd')
        try:
            check=DataOwnerModel.objects.get(email=email,pwd=pwd)
            if check.status=="Accepted":
                request.session['dataowner_id']=check.dataowner_id
                messages.info(request,'Successfull Login')
                return redirect('dataowner-home')
            else:
                messages.error(request,'Account is not Authorized')
                return redirect("dataowner-login")
        except:
            messages.warning(request,'Invalid Credentials')

    return render(request,'main/dataowner-login.html')




def dataowner_home(request):
    return render(request,'main/dataowner-home.html')



def dataowner_upload(request):
    dataowner=request.session['dataowner_id']
    data=DataOwnerModel.objects.get(dataowner_id=dataowner)
    # encrp=UploadModel.objects.get(file_id=dataowner)
    # file=encrp.id
    # print(file)

    # img=UploadModel.objects.get(id=file)
    # print(img.image)
    
    if request.method == "POST" and 'image' in request.FILES:

        file_id=request.POST.get('filenum')
        imagename=request.POST.get('imagename')
        image=request.FILES['image']
        file_name=image.name
        tags=request.POST.get('tags')
        dataowner_id=data

        key =Fernet.generate_key()
        print(repr(key),'keyyyyyy')
        d=key.decode()
        print(d,'decoded key')
        f=Fernet(d.encode('ascii'))
        print(f,'fernettttt')
        # key=random.randint(1111,9999)
        # print(key)

        key_hash = md5(d.encode('ascii')).digest()

        tdes_key = DES3.adjust_key_parity(key_hash)
        print(tdes_key)
        
        cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')

        # with open(os.path.abspath('media/' + str(image)).replace("\\","/"), 'rb') as input_file:
        #     file_bytes = input_file.read()

        # new_file_bytes = cipher.encrypt(file_bytes)

        # with open(os.path.abspath('media/' + str(image)).replace("\\","/"), 'wb') as output_file:
        #     output_file.write(new_file_bytes)
        # print('Operation Done!')

        obj = UploadModel.objects.create(imagename=imagename,image=image,tags=tags,dataowner_id=dataowner_id,encrpyt_key=d,file_id=file_id,file_name=file_name)
        messages.warning(request,'uploaded successfully')
        print(file_name)
        print(os.path.abspath(file_name))

        enc=open(os.path.abspath('media/' + str(obj.image)).replace("\\","/"), 'rb')
        img=enc.read()
        print(img,'image dataaa')
        print(type(img),'typeeee')
        print(len(img),'length')
        string_data = str(img)
        print(type(string_data),'stringsss')
        print(len(string_data),'length string')
        key = "sfa84df54d5fj5j96gfr"

        #Creating Initial block
        initial_block = HashDataBlock(key, [string_data])
        print(initial_block.block_hash, 'hash')

        #Creating Second block
        second_block = HashDataBlock(initial_block.block_hash, [imagename])
        print (second_block.block_hash)

        #Creating Third block
        third_block = HashDataBlock(second_block.block_hash, [file_name])
        print (third_block.block_hash)
        enc.close()

        obj.image_block = initial_block.block_hash
        obj.imagename_block = second_block.block_hash
        obj.file_name_block = third_block.block_hash
        obj.save()
        # encrypted=f.encrypt(img)

        # dec = open('media/' + str(obj.image), 'wb')
        # dec.write(encrypted)
        # dec.close()
                
        
        return redirect('dataowner-home')


    return render(request,'main/dataowner-upload.html')



def upload(request,id):

    img=UploadModel.objects.filter(file_id=id)
    return redirect('dataowner-upload',{'img':img})


def dataowner_request(request):
    owner_id=request.session['dataowner_id']
    req=RequestModel.objects.filter(owner_id=owner_id)
    # print(req)

    return render(request,'main/dataowner-request.html',{'req':req})



def accept_generate_key(request,id):

    def key_generator(size=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + '!@#$%^&*()_+?~'):
        return ''.join(random.choice(chars) for _ in range(size))

    key = key_generator()
    print(key)
    RequestModel.objects.filter(request_id=id).update(key=key,status='Accepted')
    email=RequestModel.objects.get(request_id=id).user_id
    print(email)
    mail=UserModel.objects.get(user_id=email).email
    print(mail)
    username=UserModel.objects.get(user_id=email).name
    print(username)
    owner=RequestModel.objects.get(request_id=id).owner_id
    print(owner)
    ownername=DataOwnerModel.objects.get(dataowner_id=owner).name
    print(ownername)

    # html_content = "<p>Hello, " + str(username) + " Your request has been <b>Accepted by </b>" + str(ownername)+ " & download the file, please <b>Enter the key </b>" + str(key) + ".</p>" 
    # from_mail = DEFAULT_FROM_EMAIL
    # to_mail = [mail]
    # # if send_mail(subject,message,from_mail,to_mail):
    # msg = EmailMultiAlternatives("Connection Status", html_content, from_mail, to_mail)
    # print(msg)
    # msg.attach_alternative(html_content, "text/html")
    # if msg.send():
    #     print("Sent")
    return redirect('dataowner-view-request')



def reject_download(request,id):
    RequestModel.objects.filter(request_id=id).update(key="Not available",status='Rejected')
    email=RequestModel.objects.get(request_id=id).user_id
    print(email)
    owner=RequestModel.objects.get(request_id=id).owner_id
    print(owner)
    mail=UserModel.objects.get(user_id=email).email
    print(mail)
    username=UserModel.objects.get(user_id=email).name
    print(username)
    ownername=DataOwnerModel.objects.get(dataowner_id=owner).name
    print(ownername)

    html_content = "<p>Hello, " + str(username) + " Your request has been <b>Rejected by </b>" + str(ownername)+ ".</p>" 
    from_mail = DEFAULT_FROM_EMAIL
    to_mail = [mail]
    # if send_mail(subject,message,from_mail,to_mail):
    msg = EmailMultiAlternatives("Connection Status", html_content, from_mail, to_mail)
    print(msg)
    msg.attach_alternative(html_content, "text/html")
    if msg.send():
        print("Sent")
    return redirect('dataowner-view-request')





def dataowner_profile(request):
    dataowner_id=request.session['dataowner_id']
    profile=DataOwnerModel.objects.filter(dataowner_id=dataowner_id)

    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        location=request.POST.get('location')
        pwd=request.POST.get('pwd')
        cpwd=request.POST.get('cpwd')

        DataOwnerModel.objects.filter(dataowner_id=dataowner_id).update(name=name,email=email,mobile=mobile,location=location,pwd=pwd,cpwd=cpwd)
        messages.info(request,'updated successfully')

    return render(request,'main/dataowner-profile.html',{'profile':profile})



def dataowner_view_upload(request):
    dataowner_id=request.session['dataowner_id']
    data=UploadModel.objects.filter(dataowner_id=dataowner_id)

    return render(request,'main/dataowner-view-upload.html',{'data':data})