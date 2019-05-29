from peewee import *
import os, sys,  datetime, time, yaml
import subprocess
from pprint import pprint
import argparse
from settings import Settings


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
    print("Could not determine db_type: %s" % settings.get('db_type'))
    sys.exit(1)


class Banlist(Model):
    # hostname = CharField(max_length=255)
    created = DateTimeField(default=datetime.datetime.now)
    # name = TextField()
    # protocol = CharField(max_length=16)
    # port = CharField(max_length=32)
    ip = CharField(max_length=64)
    jail = CharField(max_length=64)

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
        print("Connecting to DB..")

        db.connect()

        print("Create tables..")
        db.create_tables([Banlist])

    def close(self):
        db.close()

    def deamon_run(self):
        print("And I was Runnin' - Forrest Gump")
        self.readlist()
        time.sleep(self.settings.get('check_interval'))

    def readlist(self):
        print("Importing current banlist")

        whenTime = datetime.datetime.now() - \
            datetime.timedelta(seconds=settings.get('findtime'))

        query = Banlist.select().where(
            Banlist.created > whenTime
        )

        for entry in query:
            self.ban(entry)

    ## Not sure if I need this, only if fail2ban won't do local iptables plus our own
    def ban(self, jail, ip):
        pprint("fail2ban-client %s set banip %s" % (entry.jail, entry.ip))
        # subprocess.check_call("fail2ban-client %s set banip %s" % (entry.jail, entry.ip))

    def add_ban(self, jail, ip):
        Banlist.create(jail=jail,ip=ip)
        pprint("DB: Jail: %s | banip %s" % (jail, ip))
        # subprocess.check_call("fail2ban-client %s set banip %s" % (entry.jail, entry.ip))
