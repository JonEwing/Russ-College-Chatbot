'''Module containing all testing helper functions
for building a test script with 'nosetest'

Contains functions for loading test cases from JSON, testing
that this module is getting called, and several tests to check
chatbot functionality in terms of response time and correctness.

@author Team TBA
'''

from chatterbot.response_selection import get_random_response
from chatterbot import ChatBot
from chatterbot import utils
from logic import build
from logic import filters
from logic import database
import json
import sys, os

class Testing:
	'''
	The Testing object contains test cases for the
	Russ Rufus chatbot

	Args:
		@param `_source` (str): A string of the JSON file containing
		@param `_test_cases` (dict): A dictionary representing a JSON object

		Holds the source of test cases, the test cases read into a
		JSON dictionary, and the chatbot to be tested
	Attributes:
		source (str): The file containing json test cases
		test_cases (dict): Russ Rufus test cases
		chatbot (ChatBot from Chatterbot): Russ Rufus chatbot
	'''
	def __init__(self, _source='', _test_cases=None):
		if not _source == '':
			self.source = _source
			self.test_cases = self.load_test_cases()
			self.chatbot = build.chatbot

	def load_test_cases(self):
		'''Return a dict of a JSON object
		
		Read in test cases from a *.json file
		'''	
		path = os.path.abspath(self.source)
		data = json.load(open(path, encoding="utf8"))
		return data
	
	def TestRunning(self):
		'''Assert that this module is reachable from the test script
		'''
		assert(True != False)
	
	def TestConfidenceInterval(self, phrase, interval):
		'''Assert that the chatbot is responding with at least
		the set confidence interval

		@param `phrase` (str): An input string for the chatbot
		@param `interval` (float): A percentage lower-bounded for
		chatbot response confidence
		'''
		response = self.chatbot.get_response(phrase)
		assert(response.confidence >= interval)

	def TestSingleTurnConvo(self, question, target):
		'''Assert that the chatbot responds to single-turn
		conversation

		@param `questions` (str): An input string for the chatbot
		@param `targets` (str): A string of the correct response to the question
		'''
		result = self.chatbot.get_response(question)
		print('Test Data: {}'.format(question))
		print('Expected Result: {}'.format(target))
		print('Actual Result: {}\r\n'.format(result))
		assert(result.text.split() == target.split())
	
	def TestMultiTurnConvo(self, questions, targets):
		'''Assert that that chatbot response to multi-turn
		conversation

		@param `questions` ([str]): A list of input strings for the chatbot
		@param `targets` ([str]): A list of correct responses to the questions
		'''
		for question, target in zip(questions, targets):
			result = self.chatbot.get_response(question)
			print('Test Data: {}'.format(questions))
			print('Expected Result: {}'.format(targets))
			print('Actual Result: {}\r\n'.format(result))
			assert(result.text.split() == target.split())
	
	def TestResponseTime(self, time_limit, phrase='Hello'):
		'''Assert that chatbot responses are returned before the
		time limit in seconds

		@param `time_limit` (int): The time-limit in seconds for
		chatbot responses
		@param `phrase` (str): An input string for the chatbot
		'''
		response_time = utils.get_response_time(self.chatbot, phrase)
		print('Test Data: {}'.format(phrase))
		print('Expected Result: {}'.format(time_limit))
		print('Actual Result: {}\r\n'.format(response_time))
		assert(response_time <= time_limit)
	
	def TestRepeatedPhrase(self, question, target):
		'''Assert that the chatbot returns the correct response
		for repeatedly entered phrases

		@param `questions` (str): An input string for the chatbot
		@param `targets` (str): A string of the correct response to the question
		'''
		for i in range(3):
			result = self.chatbot.get_response(question)
			print('Test Data: {}({})'.format(question, i))
			print('Expected Result: {}'.format(target))
			print('Actual Result: {}\r\n'.format(result))
			assert(result.text.split() == target.split())	

	def TestCorpus(self, question, target):
		'''Assert that the chatbot responds to every single-phrase in our Russ College corpus

		@param `questions` (str): An input string for the chatbot
		@param `targets` (str): A string of the correct response to the question
		'''
		result = self.chatbot.get_response(question)
		if not (result.text.split() == target.split()):
			print("{} failed to return {}; Expected {}".format(question, target, result.text))
		else:
			print("{} returns {}; Expected {}".format(question, target, result.text))
