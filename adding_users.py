#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 08:42:01 2023

@author: mutua
"""
#Import packages
import requests
import pandas as pd
from dotenv import load_dotenv
import os 

#Load credentials 
load_dotenv()
username = os.environ.get('username')
password = os.environ.get('password')
host_api_session = os.environ.get('host_api_session')

#Read in the files with emails and names
#Format of the file col1: first_name col2: last_name col3:email
emails_data = pd.read_csv("/home/mutua/Documents/metabase_api/email_data.csv")

#Testing
#emails_data = emails_data.head()

#Get a token from metabase: Fill in the correct credentials
res = requests.post(host_api_session, 
                    headers = {"Content-Type": "application/json"},
                    json =  {"username": username, 
                             "password": password})

#Confirm  token generation and store it
assert res.ok == True
token = res.json()['id']
#using the user interface
API_ENDPOINT = os.environ.get('host_user')

#The create users in metabase
for index, row in emails_data.iterrows():
    #create Json file
    data = row.to_dict()
    r = requests.post(url = API_ENDPOINT, json = data,  headers = {'Content-Type': 'application/json',
                            'X-Metabase-Session': token})
    print(r.text)

 

#Using Pthon API wrapper to pull all users and assign to a group.  
from metabase import Metabase

metabase = Metabase(
    host=os.environ.get('host'),
    user=username,
    password=password,
)


from metabase import User,PermissionMembership
# get all objects
users = User.list(using=metabase)

#print all user emails
for user in range(len(users)):
  user_email = users[user].email
  user_id = users[user].id

  if user_email in list(emails_data.email):

      try:
          #Add user to Duka group
          PermissionMembership.create(group_id=3, user_id=user_id, using=metabase,)
          print("Added ", user_email, "to duka group")

      except:
           print("Already added", user_email)      
  else:
      print("Don't add to Duka Group")
      


