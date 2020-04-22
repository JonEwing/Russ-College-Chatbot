"""
A ChatterBot logic adapter that returns weather information from DarkSky.
"""
from chatterbot.logic import LogicAdapter
from logic.web_scraper import WebScraper
#import datetime

"""
TODO:
- From weekly forecast, map days in forecast to visitation days
- - Convert UNIX epoch timestape with the following:
	'>>> datetime.datetime.fromtimestamp(1284286794)'
	'datetime.datetime(2010, 9, 12, 11, 19, 54)'
"""


# Lat, Long (Athens, OH): 39.3292° N, 82.1013° W -> (39.329167, -82.096111)
# Dark Sky API key: 3506aecd56cf5609cab1858563b78ed0
# API_endpoint = 'https://api.darksky.net/forecast/{API Key}/{Lat},{Lon}'

class WeatherAdapter(LogicAdapter):
	"""
	A logic adapter that returns a forecast sourced from 
	Dark Sky's api.
	"""

	def __init__(self, chatbot, **kwargs):
		super(WeatherAdapter, self).__init__(chatbot, **kwargs)
	
	def can_process(self, statement):
		words = ['day', 'visit']
		if all(x in statement.text.split() for x in words):
			return True
		else:
			return False

	def process(self, input_statement, additional_response_selection_parameters):
		from chatterbot.conversation import Statement

		forecast_json = self.get_forecast()
		weekly_forecast_summary = forecast_json['summary']
		weekly_forecast_summary = weekly_forecast_summary.lower()
		
		response_text = self.get_forecast_response_str(weekly_forecast_summary)
		response_statement = Statement(text=response_text)
		response_statement.confidence = 1
		
		return response_statement

	def get_forecast(self):
		import requests
		import json

		req = requests.get('https://api.darksky.net/forecast/{}/{},{}'.format('3506aecd56cf5609cab1858563b78ed0', '39.329167', '-82.096111'))
		json_parse = req.json()
		return json_parse['daily']

	def get_forecast_response_str(self, forecast_summary):
		import random

		responses = [
			"If you plan on visiting, the weather in Athens, OH will be...{}",
			"Visiting Ohio University this week, the weather will be {}",
			"Visits this week to Athens can expect {}"
		]
		
		response = random.choice(responses)
		print(response)
		print(forecast_summary)
		response = response.format(forecast_summary)
		print(response)
		return response