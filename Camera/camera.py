import random, threading, time, json, datetime
from requests.exceptions import Timeout
import requests

# map of numbers to mock camera inputs
options = {0 : "Move Left",
           1 : "Move Right",
           2 : "Move Up",
           3 : "Move Down",
           4 : "Detected Motion",
           5 : "User Began Viewing",
           6 : "Brightness Up",
           7 : "Brightness Down",
}   

List = []

def post_data():
    payload = {'logs': List}
    print payload 
    resp = requests.post('http://127.0.0.1:5000/dump/', json=json.dumps(payload))
    if not resp.ok:
        print resp.json() 

def open_conn():
    try:
        resp = requests.get(url = "http://127.0.0.1:5000/updates/", timeout=10)
        print resp 
        if resp.ok:
            post_thread = threading.Thread(target=post_data) #kicks off post thread to send logs to server
            post_thread.start()
    except Timeout as ex:
        print "API Server did not respond. Expected behavior. Retrying..."
    open_conn()

#simply sets off a thread to append random data every 10 seconds 
def mock_data_stream():
    num = random.randint(0,7)
    List.append(options[num] + ". " + str(datetime.datetime.utcnow()))
    threading.Timer(10, mock_data_stream).start()

if __name__ == '__main__':
    mock_data_stream()
    open_conn()