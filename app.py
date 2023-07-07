from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)
import pandas as pd
from threading import Thread
import threading
import time
import requests
import websocket
from api_helper import ShoonyaApiPy
from NorenRestApiPy.NorenApi import NorenApi
import pyotp
import traceback
import pandas as pd
import os
import pytz

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



FINsymbol =""
enteredPremium = ""
wsfintradeat = 0.0

#import gunicorn
username = ''
raja_username = ''
am_username = ''
strikeCE = ''
strikePE = ''
fnlot = 1
printcount = 0
BankNiftyIndex = 0.0
FINiftyIndex = 0.0
#pipreqs . pip install pipreqs


app = Flask(__name__)
app.config['INITIAL_TEXT'] = 'Initial text'  # Initial text value

returntext = ""
rajacount = 0
amcount = 0
uid = str('FA75410')
pwd = str('Nar7@198983')
factor2 = str('15-04-1983')
vc = str('FA75410_U')
app_key = str('29ae32c0f6585938605c4ca65258fdd8')
imei = str('abc1234')
totptoken = 'LT4742H72JRUS5H27442C426PB2747G7'
totp = pyotp.TOTP(totptoken).now()
print(totp)


IST = pytz.timezone('Asia/Kolkata')

FINCESTRIKEATMAt = 0
FINcevalueATMAt = 0
FINPESTRIKEATMAt =0
FINpevalueATMAt =0
isFinChecked = False

FinvasiaClient = ShoonyaApiPy()
def FinvasiaLogin():
    try:
        global FinvasiaClient
        global isTeleError
        global FINnumarraystk
        #time.sleep(60)
        #start of our program

        FinvasiaClient.login(userid=uid,
                             password=pwd,
                             twoFA=totp,
                             vendor_code=vc,
                             api_secret=app_key,
                             imei=imei)

        if FinvasiaClient is not None:
            print("Login Success....")
            #print("I am alive:....Waiting for Telegram Signal....")
            FINnumarraystk = []
            FINfirststk = int(wsfintradeat) - 500
            while FINfirststk != int(wsfintradeat) + 500:

                FINpestk = FinvasiaClient.searchscrip(exchange="NFO",
                                                        searchtext=FINsymbol + 'P' +
                                                        str(FINfirststk))
                FINcestk = FinvasiaClient.searchscrip(exchange="NFO",
                                                        searchtext=FINsymbol + 'C' +
                                                        str(FINfirststk))

                if 'None' not in str(FINpestk) and 'None' not in str(FINcestk):
                    FINstkitem = {
                    'pestkitem': {
                        'strik': str(FINfirststk),
                        'strikvalue': pd.DataFrame(FINpestk).iloc[0][1]['token']
                    },
                    'cestkitem': {
                        'strik': str(FINfirststk),
                        'strikvalue': pd.DataFrame(FINcestk).iloc[0][1]['token']
                    }
                    }
                    FINnumarraystk.append(FINstkitem)
                FINfirststk = FINfirststk + 50
            print("Strikes Count: " + str(len(FINnumarraystk)))
            return "Login Success...."
        else:
            print("Login failed1, algo restarting....")
            FinvasiaLogin()
            return "Login failed2, app restarting...."
    except:
        print("Login failed3, algo restarting....")
        print(traceback.format_exc())

        FinvasiaLogin()
        pass

        return "Login failed4, algo restarting...."
FinvasiaLogin()





@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def update_text_background_task():
    with app.app_context():
        #command = ["python", "gsheet.py"]
        #subprocess.run(command)
        while True:
            # Perform any necessary data updates here
            updated_text = 'Updated text: ' + str(time.time())
            app.config['INITIAL_TEXT'] = updated_text
            time.sleep(1)  # Wait for 1 second before the next update

def AdjustExecuteOrders(orderstrick, orderlot, orderprice, buysell):
  global FinvasiaClient
  print('order received')

  try:
    if orderprice == '0' or orderprice == '0.0' :
      pricetype = 'MKT'
      priceo = 0
    else:
        if buysell == 'B':
            orderprice = str(float(orderprice) + 5)

        if buysell == 'S':
            orderprice = str(float(orderprice) - 5)

        pricetype = 'LMT'
        priceo = orderprice

    if orderlot == 0:
      orderlot = 0

   

    order1 = FinvasiaClient.place_order(
      buy_or_sell=buysell,
      product_type='I',
      exchange='NFO',
      tradingsymbol= orderstrick,
      quantity=orderlot,
      discloseqty=0,
      price_type=pricetype,
      price=orderprice,
      retention='DAY',
      #amo='Yes',
      remarks='my_order_001')
    print(order1)
    return order1
  except:
    print("except occur & retry")
    print(traceback.format_exc())
    pass



@app.route('/entryFin')
def entryFin():
    global strikeCE
    global strikePE

    order1 = AdjustExecuteOrders(str(strikeCE), 40 * fnlot,
                              str(float(0)), 'S')
    order2 = AdjustExecuteOrders(str(strikePE), 40 * fnlot,
                              str(float(0)), 'S')
    return jsonify(text=(str(str(order1["norenordno"])+"--" + str(order2["norenordno"]))))

@app.route('/exitFin')
def exitFin():
    global strikeCE
    global strikePE

    order1 = AdjustExecuteOrders(str(strikeCE), 40 * fnlot,
                              str(float(0)), 'B')
    order2 = AdjustExecuteOrders(str(strikePE), 40 * fnlot,
                              str(float(0)), 'B')
    return jsonify(text=(str(str(order1["norenordno"])+"--" + str(order2["norenordno"]))))

@app.route('/getprofitraja75410')
def getprofitraja75410():
    global rajacount
    global returntext
    global strikeCE
    global strikePE
    global all_strikes
    global printcount
    global FINCESTRIKEATMAt
    global FINPESTRIKEATMAt
    global BankNiftyIndex
    global FINiftyIndex
    global FINcevalueATMAt
    global FINpevalueATMAt
    global FINsymbol
    global wsfintradeat
    global enteredPremium
    global isFinChecked

    all_strikes = []
    FINCESTRIKEATMAt = int(wsfintradeat)
    FINPESTRIKEATMAt = int(wsfintradeat)
    FINactivestik_p = ''
    all_strikes.append('26009')
    all_strikes.append('26037')
    for s in FINnumarraystk:
        if s['pestkitem']['strik'] == str(FINPESTRIKEATMAt):
            FINactivestik_p = str(s['pestkitem']['strikvalue'])
            FINpetokenATMAt = str(s['pestkitem']['strikvalue'])
            all_strikes.append(FINactivestik_p)
            FINactivestik_p = ''
            break
    for s in FINnumarraystk:
        if s['cestkitem']['strik'] == str(FINCESTRIKEATMAt):
            FINactivestik_c = str(s['cestkitem']['strikvalue'])
            FINcetokenATMAt = str(s['cestkitem']['strikvalue'])
            all_strikes.append(FINactivestik_c)
            activestik_c = ''
            break

    totalcount = len(all_strikes)
    for s in all_strikes:
        if s == '26009' or s == '26037':
            ret = FinvasiaClient.get_quotes(exchange="NSE", token=s)
            if ret != 'NoneType':
                TOKEN = ret['token']
                LTP = ret['lp']

                if TOKEN == '26009':  #and LTP != '0':
                    BankNiftyIndex = int(float(LTP))

                if TOKEN == '26037':  #and LTP != '0':
                    FINiftyIndex = int(float(LTP))

        else:
            ret = FinvasiaClient.get_quotes(exchange="NFO", token=s)
            if ret != 'NoneType':
                TOKEN = ret['token']
                LTP = ret['lp']
                if TOKEN == str(FINpetokenATMAt):
                    FINpevalueATMAt = float(LTP)

                if TOKEN == str(FINcetokenATMAt):
                    FINcevalueATMAt = float(LTP)

    LTP = 0
    TOKEN = 0
    if printcount == 2:
        printcount = 0
        #os.system('clear')
    trademessage = str(FINCESTRIKEATMAt) + " CE " + str(
        FINcevalueATMAt) + " " + str(FINPESTRIKEATMAt) + " PE " + str(
        FINpevalueATMAt) 
    print(trademessage)

    printcount = printcount + 1
    #ltpsubscribe(all_strikes)
    
    #while True:
    runningcount = 0
    strategycm2m = 0.0
    runningpositions = FinvasiaClient.get_positions()
    if not (runningpositions is None):
        runningpositions = pd.DataFrame(runningpositions)
        runningpositions = runningpositions.reset_index()
        
        allm2m = 0.0
        strikeCE = ''
        strikePE = ''
        cem2mquantity = 0
        pem2mquantity = 0
        tartgetm2m = 0
        returntext = ""
        sl =0
        tm2m = 0
        roi = 0
        capital = 0
        rpnl = 0 
        cem2m = 0
        pem2m = 0
        BNsymbol = ""
        FINsymbol = ""
        wsbntradeat = ""
        wsfintradeat = 0.0
        enteredPremium = ""
        
        with open('gsheet.txt', 'r') as file:
            gsheetdata = file.read()
            gsheetdata = gsheetdata.split('~')
            if(len(gsheetdata) == 5):
                BNsymbol = str(gsheetdata[0])
                FINsymbol = str(gsheetdata[1])
                wsbntradeat = int(float(gsheetdata[2]))
                wsfintradeat = int(float(gsheetdata[3]))
                enteredPremium = str(gsheetdata[4])

        for index, row in runningpositions.iterrows():
            #allm2m = allm2m +  float(row['urmtom'])
            
            if (row['netqty'] != '0' and str(wsfintradeat) in row['tsym'] and 'M' in row['prd']):
                #print(row['tsym'], row['netqty'], row['urmtom'] )
                rpnl = float(rpnl) + float(row["rpnl"])
                
                if 'C' in row['tsym']:
                    strikeCE = row['tsym']
                    cem2mquantity = str(row['netqty'])
                    sl = (int(cem2mquantity))/40
                    sl = sl * 2651
                    capital = (int(cem2mquantity))/40
                    capital = capital * 130000
                    cem2m = str(float(row['urmtom']))
                    strategycm2m = strategycm2m +  float(cem2m) 
                    if (returntext != ""):
                        returntext = returntext +"~"+ strikeCE + "~" + cem2mquantity + "~" + cem2m 
                    else:
                        returntext = returntext + strikeCE + "~" + cem2mquantity + "~" + cem2m 

                if 'P' in row['tsym']:
                    strikePE = row['tsym']
                    pem2mquantity = str(row['netqty'])
                    sl = (int(pem2mquantity))/40
                    sl = sl * 2600
                    capital = (int(cem2mquantity))/40
                    capital = capital * 130000
                    pem2m = str(float(row['urmtom'])) 
                    strategycm2m = strategycm2m +  float(pem2m)
                    if (returntext != ""):
                        returntext = returntext + "~" + strikePE + "~" + pem2mquantity + "~" + pem2m 
                    else:
                        returntext = returntext + strikePE + "~" + pem2mquantity + "~" + pem2m
        
        runningpositions = runningpositions.loc[runningpositions['netqty'] != '0']
        urmtom = runningpositions.loc[runningpositions['urmtom'] != '0']
        
        runningcount = len(runningpositions.index)
        capital = float( str.replace(str(capital), '-', ''))
        
        if capital != 0 and strategycm2m != 0:
            strategycm2m = rpnl + strategycm2m
            strategycm2m = round(strategycm2m, 2)
            strategycm2m = strategycm2m + + float(rpnl)
            
            roi = int(strategycm2m)/(int(capital))
            roi = roi * 100
            roi = round(roi, 2)
            if "-" in str(strategycm2m) and "-" in str(sl):
                if sl > strategycm2m and runningcount > 0:
                    runningcount = 0
                    exitFin()
        else:
            roi = 0
        if strikeCE == "":
            if (returntext != ""):
                        returntext = returntext +"~"+ strikeCE + "~" + str(cem2mquantity) + "~" + str(cem2m) 
            else:
                returntext = returntext + strikeCE + "~" + str(cem2mquantity) + "~" + str(cem2m)
        if strikePE == "":
            if (returntext != ""):
                        returntext = returntext + "~" + strikePE + "~" + str(pem2mquantity) + "~" + str(pem2m) 
            else:
                returntext = returntext + strikePE + "~" + str(pem2mquantity) + "~" + str(pem2m)

        returntext = returntext + "~" + str(strategycm2m) + "~" + str(sl) + "~" + str(roi) + "~" + str(int(capital)) + "~" + str(int(FINiftyIndex)) + "~" + str(int(BankNiftyIndex)) + "~" + str(enteredPremium)
    rajacount = rajacount + 100
    print(str(strategycm2m+rajacount))
    #return jsonify(text=(str(returntext+rajacount)))
    return jsonify(text=(str(returntext)))
@app.route('/getprofitam44006')
def getprofitam44006():
    global amcount
    #while True:
    runningcount = 0
    strategycm2m = 0.0
    
    amcount = amcount + 1
    print(str(amcount))
    return jsonify(text=(str(strategycm2m+amcount)))


@app.route('/hello', methods=['POST'])
def hello():
    global username
    global raja_username
    global am_username
    username = request.form.get('username')
    filedata = ''
    
    if username == '198983':
       raja_username = username
       print('Request for hello page received with username=%s' % username)
       return redirect(url_for('raja75410'))
    
    if username == '1960':
        am_username = username
        print('Request for am_44006 page received with username=%s' % username)
        return redirect(url_for('am75410'))
    else:
       print('Request for hello page received with no username or blank username -- redirecting')
       redirect(url_for('index'))

@app.route('/raja75410')
def raja75410():
    global username
    if username == '198983':
       raja_username = username
       print('Request for hello page received with username=%s' % username)
       return render_template('hello.html', username = username)
    
    else:
       print('Request for hello page received with no username or blank username -- redirecting')
       return redirect(url_for('index'))
    
@app.route('/am75410')
def am75410():
    global username
    if username == '44006':
        am_username = username
        print('Request for am_44006 page received with username=%s' % username)
        return render_template('am_44006.html', username = username)
    else:
       print('Request for hello page received with no username or blank username -- redirecting')
       return redirect(url_for('index'))

@app.route('/fincheckboxchange', methods=['POST'])
def fincheckboxchange():
    global isFinChecked
    data = request.get_json()
    isFinChecked = data['isChecked']
    # Handle the checkbox state change
    # ...

    # Return a response
    response = {'message': 'Checkbox state changed successfully'}
    return jsonify(response)

@app.route('/getgsheetdata')
def getgsheetdata():
    global BNsymbol
    global FINsymbol
    global wsbntradeat
    global wsfintradeat
    global enteredPremium
    global printcount

    printcount = printcount + 1
    FINsymbol =""
    enteredPremium = ""
    wsfintradeat = 0.0
    ws = wb.worksheet('Data')
    BNsymbol = str(ws.cell(2, 1).value)
    FINsymbol = str(ws.cell(3, 1).value)
    wsbntradeat = str(ws.cell(4, 1).value)
    wsfintradeat = int(float(ws.cell(5, 1).value))
    enteredPremium = str(ws.cell(6, 1).value)
    print(BNsymbol)
    print(FINsymbol)
    print(wsbntradeat)
    print(wsfintradeat)
    print(enteredPremium)
    isstoptrade = False
    with open('gsheet.txt', 'w') as file:
        file.write(str(BNsymbol+"~"+FINsymbol+"~"+wsbntradeat+"~"+str(wsfintradeat)+"~"+enteredPremium))
    #time.sleep(5)
    return jsonify(str(printcount))


if __name__ == '__main__':
    bg_task = Thread(target=update_text_background_task)
    bg_task.daemon = True
    bg_task.start()
    
    
    app.run()
