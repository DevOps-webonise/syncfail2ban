#!/usr/bin/env python3

from pprint import pprint
from peewee import Model, CharField, DateTimeField, TextField, IntegrityError
import sys
import argparse
from settings import Settings
from app import App

"""
This command adds a jailed ip to the centralized db
"""

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=True,
                    help="config file for this service")

ap.add_argument("-j", "--jail", required=True,
    help="jail name")

ap.add_argument("-i", "--ip", required=True,
    help="ip address")

args =  vars(ap.parse_args())

settings = Settings.get_config(args['config'])

app = App(settings=settings)
app.initialize()
try:
    app.add_ban_to_list(args['jail'], args['ip'])
except IntegrityError as e:
    #print("Exception %s" % str(e))
    # already exists
    sys.exit(1)
