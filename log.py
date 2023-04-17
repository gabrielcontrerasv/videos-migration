import logging
import datetime

"""
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')
"""

def getLog():
    now = datetime.datetime.now()
    date_string = now.strftime('%Y-%m-%d_%H-%M-%S')

    logger = logging.getLogger('webex_videos')
    logger.setLevel(logging.DEBUG)

    log_file_name = f'logs/log_{date_string}.log'
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
