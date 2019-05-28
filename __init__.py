from syncfail2ban import syncfail2ban
from pprint import pprint

if __name__ == "__main__":
  #pprint(syncfail2ban)
  sync = syncfail2ban("mysql+pymysql://root:s@ndb0x!@10.0.2.2/syncfail2ban")
