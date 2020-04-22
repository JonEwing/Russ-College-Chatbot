import sqlite3
from tools import db_logger

db_log = db_logger.DBLogger('db.log')
logger = db_log.logger

db_name = 'ChatbotDB.db'
conn = sqlite3.connect(db_name)
logger.info("Connected to {}".format(db_name))

c = conn.cursor()

def create_feedback_table():
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
            (User_Question TEXT, Feedback TEXT)
            ''')
    logger.info("Creating `feedback` table")

def insert_user_feedback(user_input, feedback): 
    c.execute('''INSERT INTO feedback
            (User_Question, Feedback)
            VALUES(?, ?)''', (user_input, feedback))
    conn.commit()
    logger.info("Inserting user feedback into {}".format(db_name))

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS good_call
                (User_Call TEXT, Bot_Responce TEXT,
                Bot_confidence TEXT, User_Name TEXT,
                User_Email TEXT, User_Satisfaction TEXT)
              ''')
    logger.info("Creating `good_call` table")

    c.execute('''CREATE TABLE IF NOT EXISTS bad_call
                (User_Call TEXT, Bot_Responce TEXT,
                Bot_confidence TEXT, User_Name TEXT,
                User_Email TEXT, User_Satisfaction TEXT)
              ''')
    logger.info("Creating `bad_call` table")

def close_db():
    logger.info("Closing the {}".format(db_name))
    conn.close()
    return
