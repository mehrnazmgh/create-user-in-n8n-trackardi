import requests
import pandas as pd
import random
import string
import logging

# Configure the logging settings
logging.basicConfig(filename='app.log', filemode='a',level=logging.DEBUG, 
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
kavenegarBaseUrl = 'https://api.kavenegar.com'

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
    mainDf = pd.read_excel(r'.\users.xlsx')
    # get required values
    firstNameUser=mainDf['firstName']
    lastNameUser=mainDf['lastName']
    emailUser=mainDf['email']
    phoneUser=mainDf['phone']

    # iterate excel file
    for i in range(len(mainDf)):
        dataLoginN8nUser = [
            {
                "email": emailUser[i]
            }
        ]
        # response from create user api n8n
        responseFromCreateUserApiN8n= requests.post(n8nBaseUrl+'/rest/users', json= dataLoginN8nUser ,headers={'Cookie':'n8n-auth='+n8nAuthCookie})
        
        #check the users not repetitive in n8n
        if(not responseFromCreateUserApiN8n.json()['data']) :
            print("user with email {} has been accepted already in n8n".format(emailUser[i]))
        
        else :
            
            logging.debug('{} in n8n is created.'.format(emailUser[i]))
            
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
            
            logging.debug('{} in n8n is created(registered)'.format(emailUser[i]))
            
            if (responseFromLoginApiTrackardi.status_code == 200):
            
                # save login cookies
                accessTokenTrackardi = responseFromLoginApiTrackardi.json()['access_token']
                
                dataLoginTrackardi = {
                        "email":emailUser[i],
                        "password":password,
                        "full_name": firstName + " " + lastName,
                        "roles" : ["developer"],
                    }
                
            
                #response from create user api trackardi
                responseFromCreateUserApiTrackardi= requests.post(trackardiBaseUrl+'/user', json= dataLoginTrackardi
                ,headers={'Authorization':'bearer '+accessTokenTrackardi})
                
                #check the users not repetitive in Trackardi
                if(responseFromCreateUserApiTrackardi.status_code == 409) : 
                    print("user with email {} already exists in Trackardi".format(emailUser[i]))
                   
                else :   
                    #export user password to excel
                    mainDf.loc[i, "password"] = password
                    mainDf.to_excel(r'.\users.xlsx', index=False)
                    
                    logging.debug('{} in Trackardi is created'.format(emailUser[i]))
       
    
                #response from send sms with kave negar
                tokenKavenegar = '7571313234546652435734733746664F316130664C30326153704A7436384C2B'
                messageKavenegar = 'your username = {} and your password = {} .'.format(emailUser[i] , password[i])
                responseFromSendSmsApiKavenegar =requests.get(kavenegarBaseUrl + '/v1/' + tokenKavenegar + '/sms/send.json?receptor=' + phoneUser[i]+ '&sender=10004624&message=' + messageKavenegar , json=
                {'receptor':phoneUser[i] ,
                 'sender':10004624 ,
                 'message': messageKavenegar
                }
                )

                print(responseFromSendSmsApiKavenegar)





