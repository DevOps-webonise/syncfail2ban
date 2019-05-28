from sqlalchemy import create_engine, UniqueConstraint, MetaData, Table, Column, Integer, String, Text, DateTime
from pprint import pprint

#engine = create_engine('sqlite:///college.db', echo = True)
#meta = MetaData()
#
#students = Table(
#   'students', meta,
#   Column('id', Integer, primary_key = True),
#   Column('name', String),
#   Column('lastname', String),
#)
#meta.create_all(engine)

class syncfail2ban(object):

  connect_str = False
  engine = False

  def __init__(self, connect_str):
    self.connect_str = connect_str
    self.connect()
    self.create_tables_if_needed()

  def connect(self):
    print("Connecting to DB..")
    engine = create_engine("%s" % (self.connect_str),echo = True)
    self.engine = engine.connect()

  def create_tables_if_needed(self):
    meta = MetaData()

    #CREATE TABLE IF NOT EXISTS `fail2ban` (
    #  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    #  `hostname` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    #  `created` datetime NOT NULL,
    #  `name` text COLLATE utf8_unicode_ci NOT NULL,
    #  `protocol` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
    #  `port` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
    #  `ip` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
    #  PRIMARY KEY (`id`),
    #  KEY `hostname` (`hostname`,`ip`)
    #) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


    fail2ban = Table(
       'fail2ban_jailed', meta,
       Column('id', Integer, primary_key = True),
       Column('hostname', String(255)),
       Column('created', DateTime),
       Column('name', Text),
       Column('protocol', String(16)),
       Column('port', String(16)),
       Column('ip', String(64)),
       UniqueConstraint('hostname','ip', name='hostname_ip')
    )

    meta.create_all(self.engine)

    pprint(fail2ban)

