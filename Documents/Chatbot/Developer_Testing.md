# Testing Guide
* [Test Coverage](#test-coverage)
* [Directory Structure](#directory-structure)
* [Testing for Developers](#testing-for-developers)

## Required Modules
|Modules|
|---|
|nosetest|
|rednose|
|xlrd|

To install nose, run:
```bash
pip install nose
```

To install rednose, run:
```bash
pip install rednose
```

To install xlrd, run:
```bash
pip install xlrd
```

## Test Coverage
##### Test Running - Confirm nose running tests
##### Confidence Interval - Confidence interval meets a minimum requirement
##### Single-turn Conversation - Single phrases return correct response
##### Multi-turn Conversation - Multiple phrases return correct responses in succession
##### Response Time - Response time meets a minimum requirement
##### Repeated Phrases - Repeated phrases return the same response
##### Russ College corpus testing - Exact phrasing of training data returns the expected response

## Directory Structure
TBA's `tests` directory contains all files required for testing
the chatterbot project. `test.py` contains the code to run nose's
tests through setup, tear-down. Calls from the nose code are run
by calling the test cases in `__init__.py`.

```bash
├── tba/
├── ChatBot/
├── tests/
└── __init__.py, test.py
```

## Testing for Developers
After cloning the repo, run the following commands from a terminal:
1. `cd tba/ChatBot`
2. `make test` (for UNIX/MAC OS) or `python3 -m nose --verbose test.py` (for Windows)

Results will be printed to the command line with failed test case ID, input, output, and the expected output. All tests will run even during test failures.
