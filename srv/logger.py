"""!
@author atomicfruitcake

@date 2020

Logging module for the gnutty server
"""

import logging
from logging.handlers import RotatingFileHandler
import sys
from srv.constants import LOG_DIR

logger = logging.getLogger("gnutty")
logger.setLevel(logging.INFO)
# handler = RotatingFileHandler(
#     filename="{}/gnutty.log".format(LOG_DIR),
#     maxBytes=200000000,
#     backupCount=3,  # 200 MB
# )
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.addHandler(logging.StreamHandler(sys.stdout))
