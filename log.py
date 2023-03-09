import logging
import datetime

# log messages
"""
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')
"""

def getLog():
    # get current date and time
    now = datetime.datetime.now()
    date_string = now.strftime('%Y-%m-%d_%H-%M-%S')

    # create logger
    logger = logging.getLogger('webex_videos')
    logger.setLevel(logging.DEBUG)

    # create file handler with current date in name
    log_file_name = f'logs/log_{date_string}.log'
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)

    return logger