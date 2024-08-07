from cryptography.fernet import Fernet
import os

key =Fernet.generate_key()
d=key.decode('utf-8')
f=Fernet(d)
    
enc=open(os.path.abspath('media/', 'rb'))
img=enc.read()
enc.close()

print(os.path.abspath('media/'))
print('file path')

encrypted=f.encrypt(img)

dec = open(os.path.abspath('media/'))
dec.write(encrypted)
dec.close()



###############################
###############################

# Encode given key to 16 byte ascii key with md5 operation
    key_hash = md5(key.encode('ascii')).digest()

    # Adjust key parity of generated Hash Key for Final Triple DES Key
    tdes_key = DES3.adjust_key_parity(key_hash)
    print(tdes_key)
    

    #  Cipher with integration of Triple DES key, MODE_EAX for Confidentiality & Authentication
    #  and nonce for generating random / pseudo random number which is used for authentication protocol
    cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')

    # Open & read file from given path
    with open(os.path.abspath('media/' + str(image)).replace("\\","/"), 'rb') as input_file:
        file_bytes = input_file.read()

    new_file_bytes = cipher.encrypt(file_bytes)

    with open(os.path.abspath('media/' + str(image)).replace("\\","/"), 'wb') as output_file:
        output_file.write(new_file_bytes)
    print('Operation Done!')