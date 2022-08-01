import re
import json, requests
from urllib import response
from wsgiref import headers
from urllib.request import urlopen
import bcrypt
import os
from random import randint
import uuid
import datetime
import smtplib


def userLocation():
    try:
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        user_data = json.load(response)
        return user_data
    except:
        return 'none'

def get_uuid_id():
    return str(uuid.uuid4())

def get_time():
    return str(datetime.datetime.now())

#hash password
def hashpassword (password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#check password
def checkpassword(password, hashedpassword):
    return bcrypt.checkpw(password.encode('utf-8'), hashedpassword.encode('utf-8'))

#Generate random number for verification
def random_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

#Send email
def send_email(email, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(os.environ.get('EMAIL'), os.environ.get('EMAIL_PASSWORD'))
        server.sendmail(os.environ.get('EMAIL'), email, message)
        server.quit()
        return 'success'
    except:
        return 'error'
