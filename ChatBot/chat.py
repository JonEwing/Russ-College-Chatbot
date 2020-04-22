from __future__ import print_function	# For Py2/3 compatibility
import eel
from logic import build
from logic import database
from tools import chatbot_logger

user_name = ''
user_email = ''
user_identity = ''

@eel.expose                         # Expose this function to Javascript
def get_name_email(user_n, user_e, user_i):
    global user_name
    global user_email
    global user_identity
    user_name = user_n
    user_email = user_e
    user_identity = user_i

@eel.expose
def userFeedback(prev_question, feedback):
    '''Input user feedback (positive or negative)

    @param prev_question (str): The last question that the
    user asked
    @param feedback (str): `success` or `fail`

    @return None
    '''
    database.insert_user_feedback(prev_question, feedback)

@eel.expose                         # Expose this function to Javascript
def js_to_py(user_input):
    '''Make the chatbot available to JavaScript code
    which will run on the server-side of a web
    connection

    @param user_input (str): A request from the user to run
    through a chatbot

    @return The chatbot's response to the user's request
    '''
    logger.info("JavaScript is running chat.py")

    # Send user input to bot, return bot response
    bot_response = chatbot.get_response(user_input)
    confidence_percent = bot_response.confidence * 100
    # Output R2's response to the chat window
    textbox_output = "{}".format(bot_response.text)
    eel.py_to_js(textbox_output, confidence_percent, user_identity)
    # Respond with Text-to-Speech if the TTS-switch is on
    eel.speak(textbox_output)
    
    logger.info(user_input)
    logger.info("Response: \"{}\" - Confidence: {}%".format(textbox_output, confidence_percent))

chatbot = build.chatbot
chat_log = chatbot_logger.ChatLogger('chat.log')
logger = chat_log.logger

database.create_table()
database.create_feedback_table()

eel.init('web')
eel.start('chatbotsite.html', options={'port': 8000, 'mode': 'user selection'}, suppress_error=True)

database.close_db()
