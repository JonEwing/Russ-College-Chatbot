import pyodbc
import pandas as pd

database = pyodbc.connect("Driver={SQL Server};SERVER=xxx;Database=xxx;UID=xxx;PWD=xxx")
unanswered_questions = pandas.read_sql('SELECT User_Call FROM bad_call',database)

unanswered_questions.to_excel('Unanswered_Question.xlsx')
