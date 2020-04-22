'''A test script for testing the chatbot (ChatBot/chat.py)
This script tests the following:
- Response Confidence
- Single-turn Conversation
- Response Time
- Repeated Phrases
- Multi-turn Conversation (not active)

Contains `nosetest` scaffolding for running tests
and tearing down after running tests

@author Team TBA
'''
from __future__ import print_function	# For Py2/3 compatibility
import tests
import rednose
import nose
from tools import test_logger


test_log = test_logger.Test_Logger('test.log')
logger = test_log.logger

TESTING = tests.Testing(_source="tests/tests.json")

def setup_module():
    print ("*********************** Module Setup ***********************\r\n")
    logger.info("Setting up testing module")
    

def teardown_module():
    print ("\r\n*********************** Module Teardown ***********************")
    logger.info("Tearing down testing module")

@nose.with_setup(setup_module, teardown_module)
def TestRunning():
    logger.info("Running tests")
    TESTING.TestRunning()

@nose.with_setup(setup_module, teardown_module)
def TestConfidenceInterval():
    logger.info("Testing Confidence Interval")
    confidence_interval = TESTING.test_cases["Confidence Interval"]["interval"]
    inputs = TESTING.test_cases["Confidence Interval"]["inputs"]
    for test_input in inputs:
        TESTING.TestConfidenceInterval(test_input, confidence_interval)

@nose.with_setup(setup_module, teardown_module)
def TestSingleTurnInteraction():
    logger.info("Testing Single-turn conversation")
    inputs = TESTING.test_cases["Single-Turn Interaction"]["inputs"]
    targets = TESTING.test_cases["Single-Turn Interaction"]["targets"]
    for test_input, target in zip(inputs, targets):
        TESTING.TestSingleTurnConvo(test_input, target)

@nose.with_setup(setup_module, teardown_module)
def TestResponseTime():
    logger.info("Testing Response Time")
    response_time = TESTING.test_cases["Response Time"]["seconds"]
    test_inputs = TESTING.test_cases["Response Time"]["inputs"]
    for test_input in test_inputs:
        TESTING.TestResponseTime(response_time, test_input)

@nose.with_setup(setup_module, teardown_module)
def TestRepeatedPhraseInteraction():
    logger.info("Testing Repeat Phrases")
    inputs = TESTING.test_cases["Repeated Phrase"]["inputs"]
    targets = TESTING.test_cases["Repeated Phrase"]["targets"]
    for test_input, target in zip(inputs, targets):
        TESTING.TestRepeatedPhrase(test_input, target)

@nose.with_setup(setup_module, teardown_module)
def TestCorpus():
    logger.info("Testing Corpus")
    inputs = TESTING.test_cases["Corpus"]["inputs"]
    targets = TESTING.test_cases["Corpus"]["targets"]
    for test_input, target in zip(inputs, targets):
        TESTING.TestCorpus(test_input, target)
