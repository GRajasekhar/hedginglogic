from telethon import TelegramClient, events
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

telekey = '5551030547:AAH6pQELunbkTCwGm4O4O372XQXOTRZvEjg'
#client = TelegramClient('RajaTeleAlgo', '7722627','a83468f1a7a200a3fa28672ef1feb7c9')


myscope = ['https://spreadsheets.google.com/feeds', 
            'https://www.googleapis.com/auth/drive']

mycred = ServiceAccountCredentials.from_json_keyfile_name('hlprj-377707-9d9ee1b7035e.json',myscope)

wsclient =gspread.authorize(mycred)
#ws = client.open("RJTRADE").sheet1
wb = wsclient.open_by_key('1Ensy2EbpfrP7ol8KEHgVcihToqD7aYtcbpSJpZiBK8Y')

ws = wb.worksheet('Data')

FINsymbol =""
enteredPremium = ""
wsfintradeat = 0.0

while True:
    BNsymbol = str(ws.cell(2, 1).value)
    FINsymbol = str(ws.cell(3, 1).value)
    wsbntradeat = str(ws.cell(4, 1).value)
    wsfintradeat = str(ws.cell(5, 1).value)
    enteredPremium = str(ws.cell(6, 1).value)
    print(BNsymbol)
    print(FINsymbol)
    print(wsbntradeat)
    print(wsfintradeat)
    print(enteredPremium)
    isstoptrade = False
    with open('gsheet.txt', 'w') as file:
        file.write(str(BNsymbol+"~"+FINsymbol+"~"+wsbntradeat+"~"+wsfintradeat+"~"+enteredPremium))
    time.sleep(5)