"""
A ChatterBot logic adapter that returns information about Ohio University Russ College tour days.
"""
from chatterbot.logic import LogicAdapter
from logic.web_scraper import WebScraper
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import bs4 as bs
import sys
import os
from pathlib import Path
from itertools import combinations

class TourAdapter(LogicAdapter):
    """
    A logic adapter that returns information sourced from 
    Wikipedia. Currently, only the 'Did you know' section
    of the main page is supported.
    """
    def __init__(self, chatbot, **kwargs):
        super(TourAdapter, self).__init__(chatbot, **kwargs)

    def can_process(self, statement):
        is_tour_question = True
        words = ['when', 'tour', 'tours', 'date', 'dates']
        combos = combinations(words, 2)
        for combo in combos:
            is_tour_question = True
            for x in combo:
                if not(x in statement.text.lower().split()):
                    is_tour_question = False
            if is_tour_question:
                return True
        return False

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_driver = os.getcwd() +"\\logic\\logic_adapters\\chromedriver.exe"
        print(os.getcwd())
        driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
        driver.get("https://admissions.ohio.edu/portal/russvisit")
        source = driver.page_source
        driver.close()

        soup = bs.BeautifulSoup(source, "html.parser")
        for tag in soup():
            tag.attrs = {
                attr: [" ".join(attr_value.replace("\n", " ").split()) for attr_value in value] 
                    if isinstance(value, list)
                    else " ".join(value.replace("\n", " ").split())
                for attr, value in tag.attrs.items()
            }

        tour_month = soup.find_all("span", class_="ui-datepicker-month")[0].get_text().strip()
        tour_year = soup.find_all("span", class_="ui-datepicker-year")[0].get_text().strip()
        tour_days = []
        for td in soup.find_all("td", class_="available"):
            tour_day = td.get_text().strip()
            tour_days.append(tour_day)
        
        response_text = 'There are tours in {} on...'.format(tour_month)
        for days in tour_days:
            response_text += ('\n\r'+tour_month+'-'+days+'-'+tour_year+',')
        response_text = response_text[:-1] + '.'

        response_statement = Statement(text=response_text)
        response_statement.confidence = 1

        return response_statement
