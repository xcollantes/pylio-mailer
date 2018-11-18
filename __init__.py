#!env/bin/python3.6

#################################################
# author: Xavier Collantes (xaviercollantes.me)
# date: November 7, 2018
# file: __init__.py
# purpose: Send email on Linux command line.
#################################################

import argparse
import yaml
import PylioMail

def main():
    # Look for input values on command line
    # IMPORTANT: Command line arguments will override config file inputs
    argParser = argparse.ArgumentParser(description="Send email on Linux command line.")
    argParser.add_argument('-t', '--to', action='store', metavar='email_address', help='email address of intented recepient')
    argParser.add_argument('-s', '--subject', action='store', metavar='subject_line', help='subject line of email')
    argParser.add_argument('-m', '--message', action='store', metavar='msg_body', help='text body of email')
    argParser.add_argument('-c', '--config-file',  action='store', default='config.yaml', metavar='path', help='path to custom configuration file')
    argParser.add_argument('-g', '--cred-file',  action='store', default='credentials.json', metavar='path', help='path to Google Gmail credentials JSON file')
    argParser.add_argument('-e', '--sender',  action='store', metavar='name', help='Google required argument; default is \'me\'')
    lineArgs = argParser.parse_args()

    # Look for input values from YAML config file 
    try:
        document = open(lineArgs.config_file, 'r')
        thisConfig = yaml.load(document)
    except FileError as e:
        print("ERROR: File Error: %s" % e)

    to = lineArgs.to if lineArgs.to != None else thisConfig['send_to']
    sender = lineArgs.sender if lineArgs.sender != None else thisConfig['sender']
    subject = lineArgs.subject if lineArgs.subject != None else thisConfig['subject']
    message = lineArgs.message if lineArgs.message != None else thisConfig['message']

    credPath = lineArgs.cred_file if lineArgs != None else thisConfig['credentials']

    myMsg = PylioMail.PylioMail(to, message, credPath, subject)
    myMsg.send()




if __name__=="__main__":
    main()
