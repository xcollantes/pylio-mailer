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
import yaml
from apiclient import errors


SCOPES = 'https://www.googleapis.com/auth/gmail.send'

## Move to external file (config)

sender = 'x'
to = '2064223441@tmomail.net'
subject = None
user = 'me'
msg = "Hello World! This is X; The time is : %s" % arrow.utcnow().to('US/Pacific').format('MMM D, YYYY H:m ZZZ')



def main():
    # Look for input values on command line
    # IMPORTANT: Command line arguments will override config file inputs  
    argParser = argparse.ArgumentParser(description="Send SMS text messages from Linux command line.")
    argParser.add_argument('-t', '--to', action='store', metavar='email_address', help='email address of recipient')
    argParser.add_argument('-s', '--subject', action='store', metavar='subject_line', help='subject line in email')
    argParser.add_argument('-m', '--message', action='store', metavar='msg_body', help='text body of email')
    argParser.add_argument('-c', '--config-file',  action='store', metavar='path', help='path to custom config file')
    argParser.add_argument('-g', '--cred-file',  action='store', metavar='path', help='path to Google credentials.json')
    lineArgs = argParser.parse_args()
    
    configPath = lineArgs.config-file
    credPath = '../mailer-cred/credentials.json' #lineArgs.cred-file
    sender = 'x'
    to = lineArgs.to
    subject = lineArgs.subject
    msg = lineArgs.message
    

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credPath, SCOPES)
        creds = tools.run_flow(flow, store)
        
    service = build('gmail', 'v1', http=creds.authorize(Http()))    
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

def test_parse():

    p = argparse.ArgumentParser(description="This is my test parser.")
    p.add_argument('--echo', '-e', action='store', metavar='output', default='no string', help='print out given arguments')
    p.add_argument('-x', '--multiply', action='store', metavar='number', default=0, type=int, help='multiplies given by 2')

    a = p.parse_args()
    print(a)
    m = a.multiply * 2
    o = a.echo

    
    print("ASSIGNMENT of E: ", a.echo)
    print("TYPE of E: ", type(a.echo))

    print('\n')
    print("ASSIGNMENT of X: ", a.multiply)
    print("TYPE of X: ", type(a.multiply))

    print("************** OUTPUTS *********************")

    if o != None:
        print("OUTPUT: %s" % o)

    if m != None:
        print(a.multiply, " x 2 = ", m)

if __name__=="__main__":
    main()


# <AMDG/>
