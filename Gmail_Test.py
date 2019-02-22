from __future__ import print_function
import mimetypes
from oauth2client import file, client, tools
import os
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
import base64
from google.oauth2 import service_account

print("STARTING DEF 1")

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    #You can add cc's and [assuming] bcc's like this:
    message['cc'] = 'james.huessy@boston.gov'
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}

print("DEF 1 COMPLETE")

print("STARTING DEF 2")

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

print("DEF 2 COMPLETE")

print("STARTING DEF 3")

def service_account_login():
  JL = json.loads(str(os.environ['SERVICE_KEY']))
  SCOPES = ['https://www.googleapis.com/auth/gmail.send']
  SERVICE_ACCOUNT_FILE = JL

  #credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  delegated_credentials = credentials.with_subject(EMAIL_FROM)
  service = build('gmail', 'v1', credentials=delegated_credentials)
  return service

print("DEF 3 COMPLETE")

print("DEF SECTION COMPLETE")
print("++++++++++++++++")
###################################################################################
#                            SENDING AN EMAIL                                     #
###################################################################################

## Calling API

service = service_account_login()

## Setting up variables that will be passed to the 'send_message' function, including the message body as string

EMAIL_FROM = 'civis.service@boston.gov'
EMAIL_TO = 'maria.borisova@boston.gov'
EMAIL_SUBJECT = 'Доброжелательная диктатура'
EMAIL_CONTENT = 'Это тест скрипта gmail. Я полагаю, что если DHS или какое-либо другое мониторинговое агентство посмотрит на это, оно их напугает.\nПриветствую наступающие Соединенные Штаты Бостона'

print("CREATING MESSAGE")

## Compiling the email

message = create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)

print("ATTEMPTING TO SEND MESSAGE")

## Sending the email

send_message(service = service, user_id = 'me', message = mg)

print("MESSAGE SENT!")

#https://developers.google.com/api-client-library/python/auth/service-accounts
#https://github.com/googleapis/google-api-python-client/issues/93
#https://stackoverflow.com/questions/32136330/where-do-i-get-the-authorized-gmail-api-service-instance-python-gmail-api



