from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
from twilio.rest import TwilioRestClient

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")
current_step = 0
end_step = 3
medical_procedure = None
PROCEDURE_KEY = "procedure"

def send_text(outgoing, body):
    # put your own credentials here
    ACCOUNT_SID = "AC3fa7dba82f00ec577cd9da96e50ee0f2"
    AUTH_TOKEN = "54ded7973a552d9fb6defccd3efac9ed"

    #client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    print(outgoing, body)

    #client.messages.create(
    #    to=outgoing,
    #    from_="+14807712950",
    #    body=body,
    #)

@app.route('/')
def homepage():
    return "hi there, how ya doin?"

@ask.launch
def start_skill():
    welcome_message = "Hi there, would you like us to notify your emergency contacts?"
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'Alerting your emergency contacts. Hold on...'
    send_text("+16025617960", "Your emergency contact is wanting to notify you.")
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = "Okay, which medical procedure would you like me to walk you through?"
    return question(bye_text)

@ask.intent("medical_intent", mapping={"procedure" : "Procedure"})
def medical_intent(procedure):
    text = "So you want help with %s." % (procedure)
    if (procedure is not None):
        session.attributes[PROCEDURE_KEY] = procedure
    else:
        return question("Sorry, I don't know that procedure. Try another one. Hope you're... okay hahaha.")

    #end_step = last_step_for(procedure)
    #instructions = get_instructions(procedure)
    return statement(text)


if __name__ == '__main__':
    app.run(debug=True)
