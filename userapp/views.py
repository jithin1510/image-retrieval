import os

from cryptography.fernet import Fernet
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render

from dataownerapp.models import UploadModel
from DataSecurity.BlockcahinAlgo import HashDataBlock
from userapp.models import *

# Create your views here.


def user_register(request):

    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        location=request.POST.get('location')
        pwd=request.POST.get('pwd')
        cpwd=request.POST.get('cpwd')

        if UserModel.objects.filter(email=email):
            messages.warning(request,'Email Already Exists')
        else:
            UserModel.objects.create(name=name,email=email,mobile=mobile,location=location,pwd=pwd,cpwd=cpwd)
            messages.info(request,'Account Created')
            return redirect('user-login')

    return render(request,'main/user-register.html')


def user_login(request):

    if request.method == "POST":
        email=request.POST.get('email')
        pwd=request.POST.get('pwd')
        try:
            check=UserModel.objects.get(email=email,pwd=pwd)
            if check.status=="Accepted":
                request.session['user_id']=check.user_id
                messages.info(request,'logged-in successfully!')
                return redirect('user-home')
            else:
                messages.error(request,'Account is not Authorized')
                return redirect("user-login")
        except:
            messages.warning(request,'Invalid Credentials')
    return render(request,'main/user-login.html')




def user_home(request):
    return render(request,'main/user-home.html')



def request_download(request,id):
    # upload_id=UploadModel.objects.get()
    user_id=request.session['user_id']
    down=UploadModel.objects.get(file_id=id)
    try:
        obj = RequestModel.objects.get(image=down.image,user_id=user_id,owner_id=down.dataowner_id.dataowner_id)
        messages.error(request, 'Request already sent for this image')
        return redirect('user-view-image')
    except:
        pass
    print(down)
    imagename=down.imagename
    print(imagename)
    owner_id=down.dataowner_id.dataowner_id
    print(owner_id)
    user_id=user_id
    print(user_id)
    image=down.image
    print(image)
    file_id=down.file_id
    file_name = down.file_name
    print(file_id)
    # req=RequestModel.objects.filter()
    RequestModel.objects.create(imagename=imagename,image=image,owner_id=owner_id,user_id=user_id,file_id=file_id,file_name=file_name)
    messages.success(request, 'Request sent successfully')

    return redirect('user-view-image')



def user_status(request):
    user_id=request.session['user_id']
    req=RequestModel.objects.filter(user_id=user_id)
    print(req)
    return render(request,'main/user-status.html',{'req':req})



def verify_file(request,id):
    user_id=request.session['user_id']
    try:
        obj=RequestModel.objects.get(request_id=id)
        file_obj = UploadModel.objects.get(file_id = obj.file_id)
        enc=open(os.path.abspath('media/' + str(file_obj.image)).replace("\\","/"), 'rb')
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
        second_block = HashDataBlock(initial_block.block_hash, [file_obj.imagename])
        print (second_block.block_hash)

        #Creating Third block
        third_block = HashDataBlock(second_block.block_hash, [file_obj.file_name])
        print (third_block.block_hash)
        enc.close()
        if file_obj.image_block == initial_block.block_hash \
        and file_obj.imagename_block == second_block.block_hash \
        and file_obj.file_name_block == third_block.block_hash:
            messages.success(request, "This is a valid Image")
            return render(request, 'main/user-download-image.html',{
                'file':file_obj,
                'block1':initial_block.block_hash,
                'block2':second_block.block_hash,
                'block3':third_block.block_hash
                })
        else:
            messages.error(request, "This Image has been Tampered")
            return redirect('user-view-status')
    except:
        messages.error(request, "This Image has been Tampered")
        return redirect('user-view-status')
    # mail=UserModel.objects.get(user_id=user_id).email
    # print(mail)
    # print('-----------------------------------')
    # img=RequestModel.objects.get(request_id=user_id).image
    # print(img)
    # print('========================')
    # print(st)
    # if request.method == "POST":
    #     key = request.POST.get('key')
    #     print(key)
    #     try:
    #         if RequestModel.objects.get(key=key):
    #             RequestModel.objects.filter(request_id=id).update(status="Verified")
    #             return redirect('user-view-status')
    #     except:
    #         return redirect('user-view-status')
    # return render(request,'main/download-file-otp.html')


def user_view_images(request):
    img=UploadModel.objects.all()


    if request.method == "POST":
        imag=request.POST.get('image')
        print('search text',imag)
        img=UploadModel.objects.filter(Q(imagename__iexact=imag)|Q(tags__icontains=imag))
        # return render(request,'main/user-view-images.html',{'img':img})

    return render(request,'main/user-view-images.html',{
        'images':img
    })



def user_profile(request):

    user_id=request.session['user_id']
    profile=UserModel.objects.filter(user_id=user_id)
    print(profile)

    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        location=request.POST.get('location')
        pwd=request.POST.get('pwd')
        cpwd=request.POST.get('cpwd')

        UserModel.objects.filter(user_id=user_id).update(name=name,email=email,mobile=mobile,location=location,pwd=pwd,cpwd=cpwd)
        messages.info(request,'updated successfully')

    return render(request,'main/user-profile.html',{'profile':profile})



def download_file(request,id):
    try:
        image=UploadModel.objects.get(file_id=id)
        print(image.imagename)

        key=image.encrpyt_key
        print(key)

        f=Fernet(key.encode('ascii'))
        print(f,'encodedddddd')
        # print(f.decrypt(key))

        with open('media/'+str(image.image) , 'rb') as img:
            decrpt=img.read()  
        print('*******************************')
        print(decrpt)
            
        decrypted=f.decrypt(decrpt)
        print(decrypted)

        with open('media/' + str(image.image), 'wb') as dec:
            dec.write(decrypted)

        print(dec)
        image.enc_status = 'Decrypted'
        image.save()

        messages.success(request, 'Image Decryption Successful')
    except:
        messages.error(request, 'Image Already Decrypted')
    return redirect('user-view-image')