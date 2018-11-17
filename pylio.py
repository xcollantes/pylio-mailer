#!env/bin/python3.6

#################################################
# author: Xavier Collantes (xaviercollantes.me)
# date: November 7, 2018
# file: pylio.py
# purpose: Send automated emails. Send SMS text messages via email. 
#################################################

from googleapiclient.discovery import build
from oauth2client import file, client, tools
from httplib2 import Http
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
import arrow
import argparse
from apiclient import errors


SCOPES = 'https://www.googleapis.com/auth/gmail.send'

def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('../mailer-cred/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
        
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    # Call to Gmail API
    sender = "jarvis.msg@gmail.com"
    to = "2064223441@tmomail.net"
    subject = ""
    user = "me"
    msg = "Hello World! this is Xavier %s" % arrow.utcnow().to('US/Pacific').format('d MMM YYYY H:M ZZZ')

    #email = "Hello World! this is Xavier (SendMsg)"
    email = CreateMsg(sender, to, subject, msg)
    
    sentMsg = SendMsg(service, user, email)
    print(sentMsg)


"""
  Sends email via Gmail API.  

  Args:
    service: Specify settings from Gmail.  
    user: Email sender email address. Can use special value 'me'.
    message: Body of email.

  Returns: Message sent. 
"""
def SendMsg(service, user, message):
    try:
        message = (service.users().messages().send(userId=user, body=message).execute())
        return message

    except errors.HttpError as e:
        print("ERROR: %s" % e)



"""
  Creates email message. 

  Args:
    sender: Email address of sender.
    to: Email address of receipient.
    subject: The email subject line.
    message_text: Body of the email.

  Returns: Object with base64url encoded email object.
"""
def CreateMsg(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    print("************** PAYLOAD *******************\n",message,"\n********************* /PAYLOAD *****************")  # DEBUG

    msg_b = base64.urlsafe_b64encode(bytes(message.as_string(), 'ascii'))
    print("AS BITSTRING: ",type(msg_b))  #DEBUG
    print("AS STRING BITSTRING",type(str(msg_b)))  #DEBUG
    return {'raw': byteStrip(msg_b)}
    #return {'raw': base64.urlsafe_b64encode(message.as_string())}  #DEBUG



"""
  Turns bytecode into string payload.

  Args: byteStr: Bytecode to be converted to string. 

  Returns: String type of encoded bytecode. 
"""
def byteStrip(byteStr):
    return str(byteStr)[2:-1]



if __name__=="__main__":
    main()



# <AMDG/>
