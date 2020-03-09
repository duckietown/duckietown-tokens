# -*- coding: utf-8 -*-
import logging

logging.basicConfig()
logger = logging.getLogger("duckietown-tokens ")
logger.setLevel(logging.INFO)

__version__ = "5.3.2"

logger.info("duckietown-tokens %s" % __version__)

from .duckietown_tokens import *
from .tokens_cli import *
