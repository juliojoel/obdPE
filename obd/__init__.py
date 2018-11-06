# -*- coding: utf-8 -*-

"""
	A serial module for accessing data from a vehicles OBD-II port

	For more documentation, visit:
	http://python-obd.readthedocs.org/en/latest/
"""

from .__version__ import __version__
from .obd import OBD
from .async import Async
from .commands import commands
from .OBDCommand import OBDCommand
from .OBDResponse import OBDResponse
from .protocols import ECU
from .utils import scan_serial, OBDStatus
from .UnitsAndScaling import Unit

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING) #DEBUG / WARNING

console_handler = logging.StreamHandler() # sends output to stderr
console_handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
logger.addHandler(console_handler)
