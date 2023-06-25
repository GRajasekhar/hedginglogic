import os
from api_helper import ShoonyaApiPy
from NorenRestApiPy.NorenApi import NorenApi
import pyotp
import traceback
import pandas as pd
#pipreqs . pip install pipreqs

count = 0
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

def getdata():
    global count
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
        #tartgetm2m = int(int(OrderQuantity) * 12)
        
        #print(runningpositions.loc[runningpositions['openbuyqty']])
        for index, row in runningpositions.iterrows():
            #allm2m = allm2m +  float(row['urmtom'])
            strategycm2m = strategycm2m +  float(row['urmtom'])
            if (row['netqty'] != '0'):
                #print(row['tsym'], row['netqty'], row['urmtom'] )
                
                
                if 'C' in row['tsym']:
                    strikeCE = row['tsym']
                    cem2mquantity = int(row['netqty'])
                if 'P' in row['tsym']:
                    strikePE = row['tsym']
                    pem2mquantity = int(row['netqty'])
            
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
        #print("Running count: " + str(runningcount))
        count = count + 100
        print(str(strategycm2m+count))
        with open('raja_75410.txt', 'w') as file:
            file.write(str(strategycm2m+count))




