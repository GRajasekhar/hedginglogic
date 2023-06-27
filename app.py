import os
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
#import gunicorn
username = ''
raja_username = ''
am_username = ''
strikeCE = ''
strikePE = ''
fnlot = 1
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
FinvasiaClient = ShoonyaApiPy()
def FinvasiaLogin():
    try:
        global FinvasiaClient
        global isTeleError
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
        while True:
            # Perform any necessary data updates here
            updated_text = 'Updated text: ' + str(time.time())
            app.config['INITIAL_TEXT'] = updated_text
            time.sleep(1)  # Wait for 1 second before the next update

def AdjustExecuteOrders(orderstrick, orderlot, orderprice, buysell):
  global FinvasiaClient
  print('order received')

  try:
    if orderprice == '0':
      pricetype = 'MKT'
      priceo = 0
    else:
      pricetype = 'LMT'
      priceo = orderprice

    if orderlot == 0:
      orderlot = 0

    if buysell == 'B':
      orderprice = str(float(orderprice) + 5)

    if buysell == 'S':
      orderprice = str(float(orderprice) - 5)

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
                              str(float(20)), 'S')
    order2 = AdjustExecuteOrders(str(strikePE), 40 * fnlot,
                              str(float(20)), 'S')
    return jsonify(text=(str(str(order1["norenordno"])+"--" + str(order2["norenordno"]))))

@app.route('/exitFin')
def exitFin():
    global strikeCE
    global strikePE

    order1 = AdjustExecuteOrders(str(strikeCE), 40 * fnlot,
                              str(float(20)), 'B')
    order2 = AdjustExecuteOrders(str(strikePE), 40 * fnlot,
                              str(float(20)), 'B')
    return jsonify(text=(str(str(order1["norenordno"])+"--" + str(order2["norenordno"]))))

@app.route('/getprofitraja75410')
def getprofitraja75410():
    global rajacount
    global returntext
    global strikeCE
    global strikePE
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
        #tartgetm2m = int(int(OrderQuantity) * 12)
        
        #print(runningpositions.loc[runningpositions['openbuyqty']])
        for index, row in runningpositions.iterrows():
            #allm2m = allm2m +  float(row['urmtom'])
            rpnl = float(rpnl) + float(row["rpnl"])
            if (row['netqty'] != '0'):
                #print(row['tsym'], row['netqty'], row['urmtom'] )
                
                
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
        # print("strikeCE: " + str(strikeCE))
        #print("pem2mquantity: " + str(pem2mquantity))
        #print("strikePE: " + str(strikePE))
        #print("cem2mquantity: " + str(cem2mquantity))
        #print("allm2m: " + str(allm2m))
        #print("strategycm2m: " + str(strategycm2m))
        #print('Total Current M2M: ' + str(cm2m) + '  Target: ' + str(tartgetm2m))
        #print("---")
        #time.sleep(60)
        runningpositions = runningpositions.loc[runningpositions['netqty'] != '0']
        urmtom = runningpositions.loc[runningpositions['urmtom'] != '0']
        
        runningcount = len(runningpositions.index)
        if capital != 0 and strategycm2m != 0:
            strategycm2m = strategycm2m + + float(rpnl)
            capital = float( str.replace(str(capital), '-', ''))
            roi = int(strategycm2m)/(int(capital))
            roi = roi * 100
            roi = round(roi, 2)
        else:
            roi = 0
        #print("Running count: " + str(runningcount))
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

        returntext = returntext + "~" + str(strategycm2m) + "~" + str(sl) + "~" + str(roi) + "~" + str(int(capital))
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



if __name__ == '__main__':
    bg_task = Thread(target=update_text_background_task)
    bg_task.daemon = True
    bg_task.start()

    app.run()
