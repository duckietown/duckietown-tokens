# -*- coding: utf-8 -*-
import logging

logging.basicConfig()
logger = logging.getLogger("duckietown-tokens ")
logger.setLevel(logging.INFO)

__version__ = "6.0.0"

logger.info("duckietown-tokens %s" % __version__)

from .duckietown_tokens import *
from .tokens_cli import *
