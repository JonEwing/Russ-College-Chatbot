"""
A ChatterBot logic adapter that returns information from Wikipedia.
"""
from chatterbot.logic import LogicAdapter
from logic.web_scraper import WebScraper
import re

class WikiLogicAdapter(LogicAdapter):
    """
    A logic adapter that returns information sourced from 
    Wikipedia. Currently, only the 'Did you know' section
    of the main page is supported.
    """
    def __init__(self, chatbot, **kwargs):
        super(WikiLogicAdapter, self).__init__(chatbot, **kwargs)
    
    def can_process(self, statement):
        words = ['...']
        if all(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        wiki_fact = self.get_wiki_fact()
        response_statement = Statement(text='Did you know{}?'.format(wiki_fact))
        response_statement.confidence = 1

        return response_statement

    def get_wiki_fact(self):
        import random
        import re as regex

        main_page = self.get_main_page()
        main_page.content = main_page.content.find('div', {'id': 'mp-dyk'}).find('ul').findAll('li')
        main_page.content = random.choice(main_page.content)
        href = main_page.find_href()
        main_page.content = main_page.scrub_tags()
        scrubbed_content = main_page.scrub_special_chars()
        return scrubbed_content

    def get_main_page(self):
        main_page = self.get_page("Main_Page")
        return main_page

    def get_page(self, subject):
        url = "https://en.wikipedia.org/wiki/{}".format(subject)
        page = WebScraper(url)
        return page