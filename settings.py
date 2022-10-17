# -*- coding: utf-8 -*-
# filename          : settings.py
# description       : Different options for parts of the program
# author            : Ian Ault
# email             : liketoaccess@protonmail.com
# date              : 04-11-2022
# version           : v1.0
# usage             :
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
PORT = 8080

# Root Plex library directory, this will set the download location for all
# media.
# The default value is "../".
ROOT_LIBRARY_LOCATION = "../"

# External API key for The Movie Database's offical API. The tmdbv3api Python
# library is used to interact with TMDb's API to insert TMDb IDs into the
# filenames
# The default value is False.
TMDB_API_KEY = False

# Enables API serving via Flask instead of Waitress. Also disables downloading
# full media and skips verification checks.
# The default value is False.
DEBUG_MODE = False
