from tools import logger

class TestLogger(logger.Logger):
    def __init__(self):
        self.fname = 'test.log'
        self.logger = logger.Logger(self.name)
