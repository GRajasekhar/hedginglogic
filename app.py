import os
from api_helper import ShoonyaApiPy
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from api_helper import ShoonyaApiPy
from NorenRestApiPy.NorenApi import NorenApi
import pyotp
import traceback
import warnings

app = Flask(__name__)

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

@app.route('/hello', methods=['POST'])
def hello():
    
    name = request.form.get('name')
    
    if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
    else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
