from pprint import pprint
from peewee import Model, CharField, DateTimeField, TextField, IntegrityError
import os, sys,  datetime, time, yaml
import subprocess
import argparse
from settings import Settings
from app import App

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
    app.add_ban(args['jail'], args['ip'])
except IntegrityError as e:
    print("Exception %s" % str(e))
    sys.exit(1)
