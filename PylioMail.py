#!env/bin/python3.6

#################################################
# author: Xavier Collantes (xaviercollantes.me)
# date: November 17, 2018
# class: PylioMail.py
# purpose: Send automated emails. 
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
import argparse
from apiclient import errors


class PylioMail:
    SCOPES = 'https://www.googleapis.com/auth/gmail.send'

    def __init__(self, to, message, credFile, subject=None, sender='me', configFile=None):
        self.to = to
        self.sender = sender
        self.subject = subject
        self.message = message
        self.configFile = configFile
        self.credFile = credFile
        self.user = sender


    """
    Sends email via Gmail API.

    Args:
      service: Specify settings from Gmail.
      user: Email sender email address. Can use special value 'me'.
      message: Body of email.

    Returns: Message sent.
    """
    def _SendMsg(self, service, user, message):
        try:
            message = (service.users().messages().send(userId=user, body=message).execute())
            return message

        except errors.HttpError as e:
            print("ERROR: %s" % e)


    """
    Turns bytecode into string payload.

    Args: byteStr: Bytecode to be converted to string.
    Returns: String type of encoded bytecode.
    """
    def _byteStrip(self, byteStr):
        return str(byteStr)[2:-1]


    """
    Creates email message.

    Args:
      sender: Email address of sender.
      to: Email address of receipient.
      subject: The email subject line.
      message_text: Body of the email.

    Returns: Object with base64url encoded email object.
    """
    def _CreateMsg(self, sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        print("************** PAYLOAD **************\n",message,"\n************** /PAYLOAD **************")

        msg_b = base64.urlsafe_b64encode(bytes(message.as_string(), 'ascii'))
        return {'raw': self._byteStrip(msg_b)}


    def send(self):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self.credFile, SCOPES)
            creds = tools.run_flow(flow, store)

        service = build('gmail', 'v1', http=creds.authorize(Http()))
        email = self._CreateMsg(self.sender, self.to, self.subject, self.message)

        sentMsg = self._SendMsg(service, self.user, email)
        print(sentMsg)


    def getMsg(self):
        return self.message


    def clearMsg(self):
        del self.message
