#!env/bin/python3.6

#################################################
# author: Xavier Collantes (xaviercollantes.me)
# date: November 7, 2018
# file: pylio.py
# purpose: Send SMS text messages via email. 
#################################################

from googleapiclient.discovery import build
from oauth2client import file, client, tools
from httplib2 import Http


SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
print(file)
def main():
    store = file.Storage('token.json')
    cred = store.get()
    if not cred or cred.invalid:
        flow = client.flow_from_clientsecrets('../mailer-cred/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
        
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    # Call to Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('Labels not found.')
    else:
        print('Labels:')
        for label in labels:
            print(label)

def test_func():
    print("TYPE: ", type(file.Storage('token.json')))
    print(file.Storage('token.json'))

if __name__=="__main__":
    main()
    #test_func()


# <AMDG/>
