import boto3
import base64

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

with open ('list', 'r') as f:
   lines = f.readlines()

for line in lines:
   values = line.strip().split(' ')
   # print(values)
   instance = values[1]
   hostname = values[3]
   print(hostname)
############################################
#############################################


def decrypt(key_text, password_data):
    key = RSA.importKey(key_text)
    cipher = PKCS1_v1_5.new(key)
    return cipher.decrypt(base64.b64decode(password_data), None).decode('utf8')

private_key_file = 'apollo.pem'
### eu-west-3 ## ATLAS
### eu-west-1 ## weazer/apollo
## ap-southeast-1 ## felix
region = 'eu-west-1'

instance_id = instance

with open(private_key_file, 'r') as key_file:
    key_text = key_file.read()

ec2_client = boto3.client('ec2', region)
response = ec2_client.get_password_data(InstanceId=instance_id)

print(decrypt(key_text, response['PasswordData']))

