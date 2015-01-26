#!/usr/bin/python

import os
from bashhub_globals import *
from model import UserContext
import dateutil.parser

def build_user_context():
    pppid = os.popen("ps -p %d -oppid=".format( os.getppid())).read().strip()

    # Non standard across systems GNU Date and BSD Date
    # both convert to epoch differently. Need to use
    # python date util to make standard.
    start_time_command = "ps -p {} -o lstart | sed -n 2p".format(pppid)
    date_string = os.popen(start_time_command).read().strip()
    date = dateutil.parser.parse(date_string)
    unix_time = int(mktime(date.timetuple()))*1000
    return UserContext(pppid, start_time, BH_USER_ID, BH_SYSTEM_ID)
