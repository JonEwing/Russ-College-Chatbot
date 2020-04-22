import logging

class Logger:
    '''A logging system for tracking chatbot building and user interactions.

    Logger will track function calls, time of running code, input,
    output, & response error and success messages.
    Arguments:
        @param `file`: The file containing a detailed log of program state.
        @param `level`: The minimum level of messages to report to file and console.
        @param `fformatter`: The output information and format to output to file.
        @param `cformatter`: The output information and format to output to console.
        
    Attributes:
        @property `logger`: A Python `logging` object that handles the output to file or console.
        @property `file_handler`: A Python `logging` object that designates file output configuration.
        @property `stream_handler`: A Python `logging` object that designates console output configuration.
    '''
    def __init__(self, fname):
        self.set_file_handler(fname)
        self.logger = self.setup(fname)

    def setup(self, fname):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.file_handler)
        logger.info('Begin logging to {}'.format(fname))
        return logger

    def set_file_handler(self, fname):
        fh = logging.FileHandler(fname)
        fh.setLevel(logging.DEBUG)
        self.set_file_format()
        fh.setFormatter(self.fformatter)
        self.file_handler = fh
    
    def set_file_format(self):
        fformat = '%(asctime)-15s | %(levelname)s | %(filename)s in %(funcName)s: %(message)s'
        self.fformatter = logging.Formatter(fformat)
    

