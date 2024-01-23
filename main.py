import requests
import pandas as pd
import random
import string
import logging

# Configure the logging settings
logging.basicConfig(filename='app.log', filemode='w',level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# password generation method
def passwordGenerator():
    passwordLength = 8
    characters = string.ascii_letters + string.digits
    password = "".join(random.choice(characters) for i in range(passwordLength))
    return password


# base urls
n8nBaseUrl = 'https://app.flowto.ir'
trackardiBaseUrl = 'https://data-api.flowto.ir'

# login admin in n8n
dataLoginAdminN8n = {
    "email": "reza.abi69@gmail.com",
    "password": "PvgE6h9AHk8TVVB"
}
responseFromLoginApiN8n= requests.post(n8nBaseUrl+'/rest/login', json = dataLoginAdminN8n)

# login admin in trackardi 
dataLoginAdminTrackardi =  {
            "username": "t.alireza99@gmail.com",
            "password": "44616518Ab"
        }
    
responseFromLoginApiTrackardi= requests.post(trackardiBaseUrl +'/user/token', data= dataLoginAdminTrackardi
, headers={'Content-Type' : 'application/x-www-form-urlencoded'})


if (responseFromLoginApiN8n.status_code == 200) :
    # save login cookies
    n8nAuthCookie = responseFromLoginApiN8n.cookies.get('n8n-auth')

    # read data from excel file 
    mainDf = pd.read_excel(r'C:\Users\p30-1\Desktop\pythonProject\creat-user\users.xlsx')
    # get required values
    firstNameUser=mainDf['firstName']
    lastNameUser=mainDf['lastName']
    emailUser=mainDf['email']

    # iterate excel file
    for i in range(len(mainDf)):
        dataLoginN8nUser = [
            {
                "email": emailUser[i]
            }
        ]
        # response from create user api n8n
        responseFromCreateUserApiN8n= requests.post(n8nBaseUrl+'/rest/users', json= dataLoginN8nUser ,headers={'Cookie':'n8n-auth='+n8nAuthCookie})
        
        # required values for register user in n8n
        firstName = firstNameUser[i]
        lastName=lastNameUser[i]
        password = passwordGenerator()
        inviterId = "9301e4a2-b1c9-4c5a-bd2f-ea9575fe8013"
        userId = responseFromCreateUserApiN8n.json()['data'][0]['user']['id']
        responseFromRegisterUserApiN8n= requests.post("https://app.flowto.ir/rest/users/" + userId, json = {
        "firstName": firstName,
        "lastName": lastName,
        "password" : password,
        "inviterId": inviterId
        })
        
        # print("n8n = " + str(responseFromRegisterUserApiN8n))
        
        logging.debug('{} in n8n is created'.format(emailUser[i]))
        
        # save login cookies
        accessTokenTrackardi = responseFromLoginApiTrackardi.json()['access_token']
        
        dataLoginTrackardi = {
                "email":emailUser[i],
                "password":password,
                "full_name": firstName + " " + lastName,
                "roles" : ["marketer"]
            }
        
    
        #response from create user api trackardi
        responseFromCreateUserApiTrackardi= requests.post(trackardiBaseUrl+'/user', json= dataLoginTrackardi
        ,headers={'Authorization':'bearer '+accessTokenTrackardi})
        
        # print("trackardi = " + str(responseFromCreateUserApiTrackardi))
        
        #export user password to excel
        mainDf["password"][i] = password
        mainDf.to_excel(r'C:\Users\p30-1\Desktop\pythonProject\creat-user\users.xlsx', index=False)
        
        logging.debug('{} in Trackardi is created'.format(emailUser[i]))
       
        
else : 
  print ("Something went wrong!!!")  




