from tools import logger
import logging

class ChatLogger(logger.Logger):
    def __init__(self, fname):
        self.set_file_handler(fname)
        self.set_stream_handler()
        self.logger = self.setup(fname)

    def setup(self, fname):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.file_handler)
        logger.addHandler(self.stream_handler)
        logger.info('Begin logging to {}'.format(fname))
        return logger

    def set_stream_handler(self):
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        self.set_console_format()
        ch.setFormatter(self.cformatter)
        self.stream_handler = ch

    def set_console_format(self):
        cformat = '%(asctime)-15s | %(levelname)s | %(message)s'
        self.cformatter = logging.Formatter(cformat)
    
class BuildLogger(logger.Logger):
    pass    
