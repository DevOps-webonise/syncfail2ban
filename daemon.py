from pprint import pprint
from peewee import Model, CharField, DateTimeField, TextField
import os, sys,  datetime, time, yaml
import subprocess
import argparse

from settings import Settings

from app import App

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=True,
                    help="config file for this service")
args =  vars(ap.parse_args())

settings = Settings.get_config(args['config'])
app = App(settings=settings)

app.initialize()

#infinite loop...
while (True):
    try:
        app.deamon_run()
    except KeyboardInterrupt:
        print("Service was Interrupted by Keyboard or SIG")
        app.close()
        sys.exit(0)
    except Exception as e:
        print("Uncaught Exception Raised." + str(e) )
        raise
