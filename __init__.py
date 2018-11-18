#!env/bin/python3.6

#################################################
# author: Xavier Collantes (xaviercollantes.me)
# date: November 7, 2018
# file: __init__.py
# purpose: Send email on Linux command line.
#################################################

import argparse
import PylioMail

def main():
    # Look for input values on command line
    # IMPORTANT: Command line arguments will override config file inputs
    argParser = argparse.ArgumentParser(description="Send email on Linux command line.")
    argParser.add_argument('-t', '--to', action='store', metavar='email_address', help='email address of intented recepient')
    argParser.add_argument('-s', '--subject', action='store', metavar='subject_line', help='subject line of email')
    argParser.add_argument('-m', '--message', action='store', metavar='msg_body', help='text body of email')
    argParser.add_argument('-c', '--config-file',  action='store', metavar='path', help='path to custom configuration file')
    argParser.add_argument('-g', '--cred-file',  action='store', metavar='path', help='path to Google credentials JSON file')
    lineArgs = argParser.parse_args()

    
    configPath = lineArgs.config_file
    credPath = '../mailer-cred/credentials.json' #lineArgs.cred_file
    sender = 'x'
    to = lineArgs.to
    subject = lineArgs.subject
    msg = lineArgs.message

    #myMsg = PylioMail.PylioMail(rec, sender,  m, cred)
    #myMsg.send()
   



if __name__=="__main__":
    main()
