from flask import Flask, current_app
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
from twilio.rest import TwilioRestClient

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")
medical_procedure = None
PROCEDURE_KEY = "procedure"
procedure_list = ["nose bleed", "nosebleed", "nose bleeds", "noses bled", "nosebleeds", "bleeding nose", "bloody nose", "nose blood",
                  "bloodienose", "bloodynose", "bloodynoses", "noseblood", "nosebloods"]

# hackathon instruction text
step0 = "sit down, and tilt head forward so that the blood drains through the nostrils."
step1 = "Compress the nose. With a finger and thumb, pinch the lower fleshy end of the nose, completely blocking the nostrils. Pinching at this point directly applies pressure at the region where the blood vessels are damaged."
step2 = "Put ice cubes in your mouth to cool yourself down. Lowering your body temperature can help reduce the blood flow to your nose."
step3 = "Wash your nose and rest. After bleeding has stopped, you can clean the area around your nose with warm water. After you have cleaned your face, you should rest for a while. This is to help to prevent further bleeding."

steps = [step0, step1, step2, step3]

current_step = 0
end_step = 4

def send_text(outgoing, body):
    # put your own credentials here
    ACCOUNT_SID = ""
    AUTH_TOKEN = ""

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    print(outgoing, body)

    client.messages.create(
        to=outgoing,
        from_="+1",
        body=body,
    )

@app.route('/')
def homepage():
    return "Welcome to our Alexa site!"

@ask.launch
def start_skill():
    welcome_message = "Hi there, would you like us to notify your emergency contacts?"
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    global current_step
    if (current_step > 0 and current_step < len(steps)):
        next_step_msg = "Next, %s" % (steps[current_step])
        if (current_step < len(steps)-1): 
            next_step_msg += " Would you like to hear the next step?"
            current_step += 1
            return question(next_step_msg)
        else:
            next_step_msg += " I hope I helped you today. Goodbye!"
            return statement(next_step_msg)
    else:
        if (current_step == end_step):
            return statement("I hope I helped you today. Goodbye!")
        else:
            response_msg = 'Alerting your emergency contacts. Hold on...'
            send_text("+1", "Your emergency contact is wanting to notify you.")
            return statement(response_msg)

@ask.intent("NoIntent")
def no_intent():
    global current_step
    if (current_step > 0):
        return statement("Okay then, have a good day.")
    else:
        bye_text = "Okay, which medical procedure would you like me to walk you through?"
        return question(bye_text)

@ask.intent("medical_intent", mapping={"procedure" : "Procedure"})
def medical_intent(procedure):
    print(procedure)
    global procedure_list
    global current_step
    if (procedure in procedure_list):
        session.attributes[PROCEDURE_KEY] = procedure
    else:
        return question("Sorry, I don't know that procedure. Please try another one.")

    #end_step = last_step_for(procedure)
    #instructions = get_instructions(procedure)
    text = "To begin treating %s, %s. Would you like to hear the next step?" % (procedure, step0)
    current_step += 1
    return question(text)


if __name__ == '__main__':
    app.run(debug=True)
