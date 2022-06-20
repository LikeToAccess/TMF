# -*- coding: utf-8 -*-
# filename          : settings.py
# description       : Different options for main.py
# author            : Ian Ault
# email             : service@nanosystems1.com
# date              : 04-11-2022
# version           : v1.0
# usage             : python main.py
# notes             : This file should not be run directly
# license           : MIT
# py version        : 3.10.2
#==============================================================================
# Sets the browser option "--headless", this will prevent the browser from
# opening a GUI window.
# Because of this, the "--disable-gpu" flag is also enabled when HEADLESS is
# set to True.
# The default value is True.
HEADLESS = True

# Sets the IP/Domain Name and port to bind the API to, the API will only be
# accessable from whatever this is set to.
# The default value is "0.0.0.0" (for localhost) and 8080.
HOST = "0.0.0.0"
PORT = 8081
