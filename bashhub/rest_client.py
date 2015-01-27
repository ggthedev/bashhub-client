#!/usr/bin/python
import json
import sys
import requests
from requests import ConnectionError
import os

from model import MinCommand
from model import StatusView
from bashhub_globals import *

def search(user_id=BH_USER_ID, limit=100, path='', query='', system_id='',
        session_name=''):

    payload = {'userId' : user_id, 'limit' : limit }

    if path:
        payload["path"] = os.getcwd()

    if query:
        payload["query"] = query

    if system_id:
        payload["systemId"] = BH_SYSTEM_ID

    url = BH_URL + "/command/v1/search"

    try:
        r = requests.get(url, params=payload)
        print(r.json())
        return MinCommand.from_JSON_list(r.json())

    except ConnectionError as error:
        print "Sorry, looks like there's a connection error. Please try again later"
        return []

def save_command(command):
    url = BH_URL + "/command"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        r = requests.post(url, data=command.to_JSON(), headers=headers)
    except ConnectionError as error:
        print "Sorry, looks like there's a connection error"
        pass

def get_status_view(user_context):
    url = BH_URL + "/client-view/v1/status"

    payload = { 'userId' : user_context.user_id, 'processId' :
            user_context.process_id, 'startTime' : user_context.start_time  }
    try:
        r = requests.get(url, params=payload)
        statusViewJson = json.dumps(r.json())
        return StatusView.from_JSON(statusViewJson)
    except ConnectionError as error:
        print("Sorry, looks like there's a connection error")
        return None

