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

ap.add_argument("-m", "--master", action="store_true",
                    help="master is in charge of cleaning old records from database")

args =  vars(ap.parse_args())

settings = Settings.get_config(args['config'])
app = App(settings=settings)

app.initialize()

#infinite loop...
while (True):
    try:
        app.deamon_run(args['master'])
    except KeyboardInterrupt:
        print("Service was Interrupted by Keyboard or SIG")
        app.close()
        sys.exit(0)
    except Exception as e:
        print("Uncaught Exception Raised." + str(e) )
        raise
