import os
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)
import pandas as pd
from threading import Thread
import threading
import time
import raja_75410
import amma_44006
import requests
username = ''
raja_username = ''
am_username = ''
#pipreqs . pip install pipreqs


app = Flask(__name__)
app.config['INITIAL_TEXT'] = 'Initial text'  # Initial text value



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

@app.route('/getprofitraja75410')
def getprofitraja75410():
    global raja_username
    global am_username
    #count = count + 1
    filedata = ''
    with open('raja_75410.txt', 'r') as file:
        filedata = file.read()
    return jsonify(text=(filedata))

@app.route('/getprofitam44006')
def getprofitam44006():
    global raja_username
    global am_username
    #count = count + 1
    filedata = ''
    
    with open('amma_44006.txt', 'r') as file:
        filedata = file.read()

    return jsonify(text=(filedata))

@app.route('/hello', methods=['POST'])
def hello():
    global username
    global raja_username
    global am_username
    username = request.form.get('username')
    filedata = ''
    
    if username == '75410':
       raja_username = username
       print('Request for hello page received with username=%s' % username)
       return redirect(url_for('raja75410'))
    
    if username == '44006':
        am_username = username
        print('Request for am_44006 page received with username=%s' % username)
        return redirect(url_for('am75410'))
    else:
       print('Request for hello page received with no username or blank username -- redirecting')
       redirect(url_for('index'))

@app.route('/raja75410')
def raja75410():
    global username
    if username == '75410':
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

def background_raja_75410_task():
    raja_75410.FinvasiaLogin()
    with app.app_context():
        while True:
            # Code to execute in the background
            # Replace with the path to your Python file
            #exec(open('raja_75410.py').read())
            raja_75410.getdata()

def background_Amma_44006_task():
    #amma_44006.FinvasiaLogin()
    with app.app_context():
        while True:
            # Code to execute in the background
            # Replace with the path to your Python file
            #exec(open('raja_75410.py').read())
            amma_44006.getdata()

if __name__ == '__main__':
    bg_task = Thread(target=update_text_background_task)
    bg_task.daemon = True
    bg_task.start()

    background_thread = threading.Thread(target=background_raja_75410_task)
    background_thread.daemon = True
    background_thread.start()

    background_thread = threading.Thread(target=background_Amma_44006_task)
    background_thread.daemon = True
    background_thread.start()

    app.run()
