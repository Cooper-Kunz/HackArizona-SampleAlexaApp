from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")

def get_headlines():
    user_pass_dict = {'user': 'sampleaccountname',
                      'passwd': 'SampleAccountPassword',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa: sampleaccountname'})
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/worldnews/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '... '.join([i for i in titles])
    return titles  
    
@app.route('/')
def homepage():
    return "hi there, how ya doin?"

@ask.launch
def start_skill():
    welcome_message = 'Hi there, is this an emergency?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'Calling 911 and alerting your emergency contacts. Hold on...'
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'what is happening then?'
    return statement(bye_text)
    
if __name__ == '__main__':
    app.run(debug=True)
