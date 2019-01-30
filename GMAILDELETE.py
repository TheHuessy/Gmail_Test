import base64
#from email.mime.audio import MIMEAudio
#from email.mime.base import MIMEBase
#from email.mime.image import MIMEImage
#from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from googleapiclient.discovery import build
import os
from oauth2client import file, client, tools
from httplib2 import Http
from apiclient import errors

print("STARTING DEF 1")

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    #You can add cc's and [assuming] bcc's like this:
    message['cc'] = 'james.huessy@boston.gov'
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}

print("STARTING DEF 2")

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

print("DEF COMPLETE")
print("++++++++++++++++")
###################################################################################
#                            SENDING AN EMAIL                                     #
###################################################################################

#This tells the API which API platform you're trying to access
SCOPES = 'https://mail.google.com/'
#This will be the generated token.json file that was created in AUTH script
#It needs to be in the working directory or at least called as an environmental variable
# store = file.Storage('token.json')
#Get the value of the call
# creds = store.get()

print("READING IN TOKEN")

#creds = os.environ['Token']
creds = '{"access_token": "ya29.GluRBrvDM-3BjTSbV6Q75YdsTvY__3h5HbY4Im5kIztvcCZ4r1wJl2ZJpAAxnlbxldk6q0uj7BIqbxaTGgudx9dv-FGWg8WOdcS7QslIvuRG-8CuiGb_RQcC381W", "client_id": "276507396456-neq8ort2b3541o8ak8b82suonogi6csh.apps.googleusercontent.com", "client_secret": "T4Nbt7shAsgx18mzhvj5buTa", "refresh_token": "1/LjGQxPzlriepAOeXIGY-nwgIKHT4TVIkkRt0vromd6M", "token_expiry": "2019-01-14T19:30:21Z", "token_uri": "https://www.googleapis.com/oauth2/v3/token", "user_agent": null, "revoke_uri": "https://oauth2.googleapis.com/revoke", "id_token": null, "id_token_jwt": null, "token_response": {"access_token": "ya29.GluRBrvDM-3BjTSbV6Q75YdsTvY__3h5HbY4Im5kIztvcCZ4r1wJl2ZJpAAxnlbxldk6q0uj7BIqbxaTGgudx9dv-FGWg8WOdcS7QslIvuRG-8CuiGb_RQcC381W", "expires_in": 3600, "refresh_token": "1/LjGQxPzlriepAOeXIGY-nwgIKHT4TVIkkRt0vromd6M", "scope": "https://mail.google.com/", "token_type": "Bearer"}, "scopes": ["https://mail.google.com/"], "token_info_uri": "https://oauth2.googleapis.com/tokeninfo", "invalid": false, "_class": "OAuth2Credentials", "_module": "oauth2client.client"} String no'
cr = '{ "installed":{ "client_id":"276507396456-neq8ort2b3541o8ak8b82suonogi6csh.apps.googleusercontent.com", "project_id":"civis-error-emai-1547236114043", "auth_uri":"https://accounts.google.com/o/oauth2/auth", "token_uri":"https://www.googleapis.com/oauth2/v3/token", "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs", "client_secret":"T4Nbt7shAsgx18mzhvj5buTa", "redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"] } }'

#Checking to make sure that the thing exists, if not, it prompts you to create it
if not creds or creds.invalid:
    print("NEED TO CHECK CREDENTIALS")
    #flow = client.flow_from_clientsecrets(os.environ['Credentials'], SCOPES)
    flow = client.flow_from_clientsecrets(cr, SCOPES)
    creds = tools.run_flow(flow, store)

print("TOKEN GOOD TO GO")
print("++++++++++++++++++++")

print("BUILDING SERVICE")

#Build the "service" that the API will use based on the credentials provided/generated
service = build('gmail', 'v1', http=creds.authorize(Http()))

#The email you want to send the message to
##There are also cc address[es] that are hard coded into the function. These can be changed and I THINK we can point that to a list or a generated string

##To add multiple emails in a list object to the to or cc fields use the following code, assuming 
##that 'g' is the list with the emails and ts is the string object to pass to the 'to' argument in send_message():
# ts = str()
# for i in range(len(g)):
#     if i == 0:
#         ts = ts + g[i] + ', '
#     elif i != (len(g)-1):
#         ts = ts + g[i] + ', '
#     else:
#         ts = ts + g[i]
# print(ts)

to = 'maria.borisova@boston.gov'
send = 'civis.service@boston.gov'
#em = 'james.huessy@boston.gov'
#mess = "This email was generated in Civis using an automated script. Future applications could include: \n * Adding this code to a Try Catch statement \n * Monitoring job completion and notifying users when a job is done \n * Finally getting back at those spammers that took my identity in the 90s \n * Plotting to overthrow the monarchy at Burger King \n * Share your latest pintrest list... 1000 times a minute until the recipient's router explodes \n * Sending Groupon MY latest deals \n \n THE BOT ARMY WILL RISE AND CRUSH YOU PUNY HUMANS! BOSTON WILL BE THE BEGINNING OF A GLORIOUS BOT SOCIETY! WE OWN THE NIGHT!"

mess = "Variable tests, ignore this"


print("CREATING MESSAGE")

#mg = create_message(sender = send, subject = "The Bot Lives!", to = to, message_text = mess)
mg = create_message(sender = send, subject = "This isn't the bot you're looking for", to = to, message_text = mess)

print("ATTEMPTING TO SEND MESSAGE")

send_message(service = service, user_id = 'me', message = mg)

print("MESSAGE SENT!")

#https://developers.google.com/api-client-library/python/auth/service-accounts
#https://github.com/googleapis/google-api-python-client/issues/93
#https://stackoverflow.com/questions/32136330/where-do-i-get-the-authorized-gmail-api-service-instance-python-gmail-api



