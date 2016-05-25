import collections
import json
import os
import random
import requests 
import sqlite3
import sys
import time 

from flask import Flask, request, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

FB_MESSAGES_ENDPOINT = "https://graph.facebook.com/v2.6/me/messages"
with open("/var/www/flask-test/fbtoken.txt", "r") as f:
    FB_TOKEN = f.readline()

random_phrases = ["cats are cool", "dogs are cool too", "hamsters are fun", "gerbils are fun too"]

userid_to_chat = collections.defaultdict(list)

class MessengerDB(object):
    """ Initialize a database to keep track of conversations with 
    FB dialogue agent """
    def __init__(self, path_to_db):
        self.conn = sqlite3.connect(path_to_db, check_same_thread=False)
        self.path_to_db = path_to_db
        c = self.conn.cursor()
        try:
            c.execute('''CREATE TABLE UserResponse (user_id text, timestamp text, response text)''')
        # Note system response table keeps track of which user it is conversing with
            c.execute('''CREATE TABLE SystemResponse (user_id text, timestamp text, response text)''')
            self.conn.commit()
        except sqlite3.OperationalError:
            None
         

    def log_response(self, agent, user_id, timestamp, response):
        """ Agent is one of 'user'/'sys' and determines
        which table we will update """
        #.conn = sqlite3.connect(self.path_to_db)
        with self.conn:
            try:
                c = self.conn.cursor()
            except Exception as e:
                None
            if agent == "sys":
                c.execute('''INSERT INTO SystemResponse VALUES (?,?,?)''', (user_id, timestamp, response)) 
            elif agent == "user":
                c.execute('''INSERT INTO UserResponse VALUES (?,?,?)''', (user_id, timestamp, response)) 

            self.conn.commit()


db = MessengerDB("/var/www/flask-test/chatbot.db")
 
#@app.route('/', methods=['GET', 'POST'])
def hub_tok_response():
    req_data = request.data
    req_args = request.args
    return req_args['hub.challenge']


@app.route('/', methods=["POST"])
def chatbot_response():
    global userid_to_chat
    global db
    curr_time = str(datetime.now())

    phrase = random.choice(random_phrases)    
    req_data = request.data
    data = json.loads(req_data)
    req_args = request.args
    sender_id = data["entry"][0]["messaging"][0]["sender"]["id"]
    sent_message = data["entry"][0]["messaging"][0]["message"]["text"]
    print "Sent message: ", sent_message
    db.log_response("user", sender_id, curr_time, sent_message)
    send_back_to_fb = {
 	    "recipient": {"id": sender_id}, "message": { "text": phrase}
    }
    print "Send back to fb: ", send_back_to_fb
    #userid_to_chat[sender_id].append(sent_message) 
    params_input = {"access_token": FB_TOKEN}
 
  
    headers = {'content-type':  'application/json'}
    # the big change: use another library to send an HTTP request back to FB
    fb_response = requests.post(FB_MESSAGES_ENDPOINT, headers=headers, params=params_input, data=json.dumps(send_back_to_fb)) 

    response_time = str(datetime.now())
    db.log_response("sys", sender_id, response_time, phrase)    
    # handle the response to the subrequest you made
    if not fb_response.ok:
        # log some useful info for yourself, for debugging
        print 'Error in response! %s: %s' % (fb_response.status_code, fb_response.text)
    # always return 200 to Facebook's original POST request so they know you
    # handled their request
    return "Ok", 200


if __name__ == '__main__':
    pass
    #app.run(host="0.0.0.0")
