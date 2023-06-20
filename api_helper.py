
from threading import Timer
import pandas as pd
import time

#subprocess.check_call([sys.executable, "-m", "pip", "install", "./NorenRestApiPy-0.0.16-py2.py3-none-any.whl"])
from NorenRestApiPy.NorenApi import  NorenApi

class SymbolItem:
    def __init__(self):
        self.df = None
        self.key = None
        self.counter  = 0
        self.lasttime = 0    

def get_time(time_string):
    data = time.strptime(time_string,'%d-%m-%Y %H:%M:%S')

    return time.mktime(data)


class ShoonyaApiPy(NorenApi):
    def __init__(self):
        #NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/', eodhost='https://api.shoonya.com/chartApi/getdata/')
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')

    
    