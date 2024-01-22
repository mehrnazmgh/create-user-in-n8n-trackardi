import requests
import pandas as pd

n8n_base_url = 'https://app.flowto.ir'
trackardi_base_url = 'https://data-api.flowto.ir'

data_login_admin_n8n = [
        {
    "email": "reza.abi69@gmail.com",
    "password": "PvgE6h9AHk8TVVB"
        }
    ]

# response_from_login_api n8n
response_from_login_api_n8n= requests.post(n8n_base_url+'/rest/login', json = data_login_admin_n8n)

if (response_from_login_api_n8n.status_code == 200) :
    
    # save login cookies
    n8n_auth = response_from_login_api_n8n.cookies.get('n8n-auth')
    
    data_login_n8n = [
        {
            "email": "pythonUser1@gmail.com"
        }
    ]
    
    #response_from_create_user_api n8n
    response_from_create_user_api_n8n= requests.post(n8n_base_url+'/rest/users', json= data_login_n8n ,headers={'Cookie':'n8n-auth='+n8n_auth})
    
    print(response_from_create_user_api_n8n.text)
      
else : 
  print ("Something went wrong!!!")
  
data_login_admin_trackardi = [
        {
    "username": "t.alireza99@gmail.com",
    "password": "44616518Ab"
        }
    ]
   
main_df = pd.read_excel(r'C:\Users\p30-1\Desktop\pythonProject\creat user\file1.xlsx')
main_phones=main_df['phone']
# print (main_phones)
input_df = pd.read_excel(r'C:\Users\p30-1\Desktop\pythonProject\creat user\file1.xlsx')
input_phones=input_df['phone']

# response_from_login_api trackardi
response_from_login_api_trackardi= requests.post(trackardi_base_url +'/user/token', data= data_login_admin_trackardi
, headers={'Content-Type' : 'application/x-www-form-urlencoded'})


if (response_from_login_api_trackardi.status_code == 200) :
    
    # save login cookies
    access_token_trackardi = response_from_login_api_trackardi.json()['access_token']
    
    data_login_trackardi = [
        {
    "email":"mehrnazmgh@gmail.com",
    "password":"mehrnaz@74",
    "full_name": "mehrnaz gheshmpour",
    "roles" : ["marketer"]
       }
    ]
    
    #response_from_create_user_api trackardi
    response_from_create_user_api_trackardi= requests.post(trackardi_base_url+'/user', json= data_login_trackardi
    ,headers={'Authorization':'bearer '+access_token_trackardi})

    print(response_from_create_user_api_trackardi.text)
    
else : 
  print ("Something went wrong!!!")    
