import os
import json
import base64
from googleapiclient.discovery import build
from apiclient import errors
from email.mime.text import MIMEText
from google.oauth2 import service_account



def send_email(Email_subject, Email_body, Email_sender='civis.service@boston.gov', Email_to='civis.service@boston.gov', Email_cc=None, Email_bcc=None):
    # Pulling in the string value of the service key from the parameter
    # Convert to json object
    JL = json.loads(os.environ['SERVICE_KEY'])


    # Define which scopes we're trying to access
    # The service account we have set up is only authorized for gmail.send
    # If we want to grant it more access, we will have to ask Patrick Collins very nicely
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    # Passing the json'd string to this object
    SERVICE_ACCOUNT_INFO = JL
    # Setting up credentials using the gmail api
    credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    # This allows us to assign an alias account to the message so that the messages aren't coming from 'ServiceDriod-8328balh blah blah'
    delegated_credentials = credentials.with_subject(Email_sender)
    # 'Building' the service instance using the credentials we've passed
    service = build('gmail', 'v1', credentials=delegated_credentials)
    

    # Building out the email
    message = MIMEText(Email_body)
    message['to'] = Email_to
    message['from'] = Email_sender
    message['subject'] = Email_subject
    # If there are CCs or BCCs provided, then they will be parsed into the right format
    if Email_cc:
        ts = str()
        for i in range(len(Email_cc)):
            if i == 0:
                ts = ts + Email_cc[i] + ', '
            elif i != (len(Email_cc)-1):
                ts = ts + Email_cc[i] + ', '
            else:
                ts = ts + Email_cc[i]
        message['cc'] = ts
    if Email_bcc:
        bts = str()
        for i in range(len(Email_bcc)):
            if i == 0:
                bts = bts + Email_bcc[i] + ', '
            elif i != (len(Email_bcc)-1):
                bts = bts + Email_bcc[i] + ', '
            else:
                bts = bts + Email_bcc[i]
        message['bcc'] = bts
    # This is important. Tutorials will just have you output as base64, but, for whatever reason, one needs to explicitly encode to UTF-8 and then call the decode to ascii
    email = {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}



    ## Function to actually send the message using the API
    try:
        message = (service.users().messages().send(userId='me', body=email).execute())
        print('Message Id: %s' % message['id'])        
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

## To test, uncomment below and run
#send_email(Email_to = "james.huessy@boston.gov", Email_subject = "Import Test", Email_body = "If this worked, then we have eliminated a few packages. \nYay!")





