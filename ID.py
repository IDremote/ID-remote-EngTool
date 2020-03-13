from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
import Reports
import subprocess
import time
import pytz

from IDsend import IDsend

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_179357125629-hi519qg1ili8qqpttoqdasaor75ou49t.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = results.get('messages', [])
    
    # Lue viestien otsikot ja IDt listaan
    for message in messages:
        messageheader= service.users().messages().get(userId="me", id=message["id"]).execute()
        
        gmailtime = int(messageheader["internalDate"]) / 1000
        date = datetime.fromtimestamp(gmailtime)

        headers=messageheader["payload"]["headers"]
        ID =  messageheader["id"]
        subject = str([i['value'] for i in headers if i["name"]=="Subject"])
        sender = str([i['value'] for i in headers if i["name"]=="From"])
        print("Otsikko:", subject)
        print("Saapumisaika:", date)
        print("Lähettäjä:", sender)

        lähettäjä = sender.split("<")
        lähettäjä = lähettäjä[1].split(">")
        lähettäjä = lähettäjä[0].replace('[','').replace(']','')
        subject = subject.replace('[','').replace(']','')

        # Poista välit, jotta muuttuja menee läpi
        otsikko = subject.replace(' ','')
        
        # Lähetä varmistusviesti
        # Kopio "Reports.py":stä. Pitää viestis olla projekti hei..
        project = ""
        if "ncl" in otsikko:
            project = "NCL"
        if "icon" in otsikko:
            project = "ICON"
        if "seabourn" in otsikko:
            project = "Seabourn"
        if project != "":
            IDsend(otsikko, lähettäjä, project, teksti)

        sekunnit = 900        
        # Ajetaan jos maili on semituore
        if time.time()-gmailtime < sekunnit:
            subprocess.call('start python Reports.py %s %s' %(otsikko,lähettäjä), shell=True)
        else:
            print("Liian vanha prosessoitavaks:", time.time()-gmailtime)
        # Archivaa maili
        try:
            service.users().messages().modify(userId="me", id=message["id"], body={'removeLabelIds': ['INBOX'],'addLabelIds': ['STARRED'],'ids': ID}).execute()
            print('Email archived.')
        except:
            print('An error occurred while archiving email.')
            exit()            

if __name__ == '__main__':
    teksti = " edc/report request received."
    start = time.time()
    timeperiod = 300
    i = 1
    runningviesti = "57:00"
    while 1 > 0:
        main()
        
        print("Seconds left before new session: {:1}".format(round(start + timeperiod - time.time(), 0)), end="\r")
        if time.time() > start + timeperiod:
            break

        #Lähetä viesti joka aamu jos on vielä pystyssä
        if datetime.now(pytz.timezone('Europe/Helsinki')).strftime("%M:%S") < runningviesti:
            i = 0
        if datetime.now(pytz.timezone('Europe/Helsinki')).strftime("%M:%S") > runningviesti:
            if i == 0:
                i = 1
                IDsend("", "markus.heinonen@fi.abb.com", "", "Vielä juostaan!")

        #Kirjota logiin
        try:
            with open(r"T:\Project Data\Projects\1CVX999999 Fincantieri NCL 1 TEST\IDremotelog.txt", "r+") as f:
                a = f.read()
                with open(r"T:\Project Data\Projects\1CVX999999 Fincantieri NCL 1 TEST\IDremotelog.txt", "w+") as f:
                    f.write(str(datetime.fromtimestamp(time.time())) +"\n" + a)
        except:
            continue
    exit()