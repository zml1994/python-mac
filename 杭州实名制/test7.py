# -*- codeing = utf-8 -*-
import requests
import random
import string
from requests_toolbelt import MultipartEncoder

token = '1170a8b0a81e40daba665ccd213269f1'
url = "http://115.233.209.232:9000/api/realname/project/importProject"
file_name = '02.xls'

fields = {"Content-Disposition": "form-data",
         "name": "file",
         "filename": file_name,
         "Content-Type": "application/wps-office.xlsx",
         "file": (file_name, open(file_name, 'rb'), 'application/vnd.ms-excel')}


boundary = '----WebKitFormBoundary'+''.join(random.sample(string.ascii_letters+string.digits, 16))
m = MultipartEncoder(fields=fields, boundary=boundary)
headers = {'Content-Type': m.content_type, 'x-access-token': token}

r = requests.post(url, data=m, headers=headers)

print(r.json())

