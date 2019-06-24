#!/usr/bin/env python3

import os, sys,  datetime, time, yaml
import logging
import subprocess
import argparse
import socket
import ipaddress
import re
from peewee import *
from pprint import pprint
from settings import Settings

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=True,
                    help="config file for this service")

#only parse known args here, as config is always needed
#args =  vars(ap.parse_args())

args, unknown = ap.parse_known_args()
args = vars(args)

settings=Settings.get_config(args['config'])

### DB CONNECTION SELECTION
if settings.get('db_type') == 'mysql':
    db = MySQLDatabase(settings.get('db_name'),
                        user=settings.get('db_user'),
                        password=settings.get('db_pass'),
                        host=settings.get('db_host'),
                        port=settings.get('db_port')
                       )

elif settings.get('db_type') == 'sqlite':
    # SQLite database using WAL journal mode and 64MB cache.
    db = SqliteDatabase(settings.get('db_path'), pragmas={
        'journal_mode': 'wal',
        'cache_size': -1024 * 64
    })

elif settings.get('db_type') == 'postgresql':
    db = PostgresqlDatabase(settings.get('db_name'),
            user=settings.get('db_user'),
            password=settings.get('db_pass'),
            host=settings.get('db_host'),
            port=settings.get('db_port')
    )
else:
    logging.error("Could not determine db_type: %s" % settings.get('db_type'), "db_type_error")
    sys.exit(1)


class Banlist(Model):
    from_hostname = TextField()
    ip = CharField(max_length=64)
    jail = CharField(max_length=64)
    created = DateTimeField(default=datetime.datetime.now)
    # since jails should match these rules should be in the jail - omitting for now
    # protocol = CharField(max_length=16)
    # port = CharField(max_length=32)

    class Meta:
        database = db
        db_table = 'banlist'
        indexes = (
          (('ip', 'jail'), True),
        )


class App():
    def __init__(self, settings):
        self.settings = settings

    def initialize(self):
        db.connect()
        db.create_tables([Banlist])

    def close(self):
        db.close()

    def deamon_run(self):
        self.readlist()

        if self.settings.get('master'):
            self.cleanlist()

        time.sleep(self.settings.get('check_interval'))

    # Only read contents that may have changed in interval time
    # otherwise we keep adding the same ips over and over, which
    # causes a persistent banning loop
    def readlist(self):
        logging.info("Reading list..")

        hostname = self.get_hostname()
        seconds = int(settings.get('check_interval'))

        whenTime = datetime.datetime.now() - \
            datetime.timedelta(seconds=seconds)

        query = Banlist.select().where(
            Banlist.created > whenTime,
            Banlist.from_hostname != hostname
        )

        for entry in query:
            logging.info("Entry: %s" % (str(entry)))
            self.ban_action(entry.jail, entry.ip, hostname)

    # Remove entries that should have been picked up by now. So entries that
    # are 2x as old as the check_interval as other servers will share this db
    # and may be a few seconds behind.
    # You only want to run this on a single server, use master config attribute
    # to enable
    def cleanlist(self):
        # So 5 second interval, means anything older than 9s
        # should have been picked up
        seconds = int(settings.get('check_interval')*2) - 1

        whenTime = datetime.datetime.now() - \
            datetime.timedelta(seconds=seconds)

        query = Banlist.delete().where(
            Banlist.created < whenTime
        ).execute()

    # Ban imported user
    def ban_action(self, jail, ip):

        ip=self.sanitize_ip(ip)
        jail=self.sanitize_jail(jail)

        logging.info("syncfail2ban: ran command 'fail2ban-client set %s banip %s'" % (jail, ip))
        os.system("/usr/bin/fail2ban-client set %s banip %s" % (jail, ip))

    # Add jail and ip to database for sharing with other clients
    def add_ban_to_list(self, jail, ip):
        logging.info("syncfail2ban: Added %s (ip) to %s (jail) to database" % (ip, jail))
        Banlist.create(jail=jail,ip=ip,from_hostname=self.get_hostname())

    def get_hostname(self):
        return socket.gethostname()

    def sanitize_ip(self, ip):
        try:
            ipaddress.ip_address(ip)
        except Exception as e:
            return false

        return ip

    def sanitize_jail(jail):

        validjail = re.search("^[a-zA-Z0-9-_]+$", jail)

        if (validjail):
            return jail

        return false
