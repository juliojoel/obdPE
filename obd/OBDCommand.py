# -*- coding: utf-8 -*-

from .utils import *
from .protocols import ECU
from .OBDResponse import OBDResponse

import logging

logger = logging.getLogger(__name__)


class OBDCommand():
    def __init__(self,
                 name,
                 desc,
                 command,
                 _bytes,
                 decoder,
                 ecu=ECU.ALL,
                 fast=False):
        self.name      = name        # human readable name (also used as key in commands dict)
        self.desc      = desc        # human readable description
        self.command   = command     # command string
        self.bytes     = _bytes      # number of bytes expected in return
        self.decode    = decoder     # decoding function
        self.ecu       = ecu         # ECU ID from which this command expects messages from
        self.fast      = fast        # can an extra digit be added to the end of the command? (to make the ELM return early)

    def clone(self):
        return OBDCommand(self.name,
                          self.desc,
                          self.command,
                          self.bytes,
                          self.decode,
                          self.ecu,
                          self.fast)

    @property
    def mode(self):
        if len(self.command) >= 2:
            return int(self.command[:2], 16)
        else:
            return 0

    @property
    def pid(self):
        if len(self.command) > 2:
            return int(self.command[2:], 16)
        else:
            return 0


    def __call__(self, messages):

        # filter for applicable messages (from the right ECU(s))
        for_us = lambda m: self.ecu & m.ecu > 0
        messages = list(filter(for_us, messages))

        # guarantee data size for the decoder
        for m in messages:
            self.__constrain_message_data(m)

        # create the response object with the raw data recieved
        # and reference to original command
        r = OBDResponse(self, messages)
        if messages:
            r.value = self.decode(messages)
        else:
            logger.info(str(self) + " did not recieve any acceptable messages")

        return r


    def __constrain_message_data(self, message):
        """ pads or chops the data field to the size specified by this command """
        if self.bytes > 0:
            if len(message.data) > self.bytes:
                # chop off the right side
                message.data = message.data[:self.bytes]
                logger.debug("Message was longer than expected. Trimmed message: " + repr(message.data))
            elif len(message.data) < self.bytes:
                # pad the right with zeros
                message.data += (b'\x00' * (self.bytes - len(message.data)))
                logger.debug("Message was shorter than expected. Padded message: " + repr(message.data))


    def __str__(self):
        return "%s: %s" % (self.command, self.desc)

    def __hash__(self):
        # needed for using commands as keys in a dict (see async.py)
        return hash(self.command)

    def __eq__(self, other):
        if isinstance(other, OBDCommand):
            return (self.command == other.command)
        else:
            return False
