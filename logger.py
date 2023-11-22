import logging
import pprint
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_handler = logging.StreamHandler(sys.stdout)
logger_handler.setLevel(logging.DEBUG)
logger.addHandler(logger_handler)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s')
logger_handler.setFormatter(formatter)


