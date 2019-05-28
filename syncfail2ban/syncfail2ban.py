from sqlalchemy import create_engine

class syncfail2ban(Object):

  def __init__(self, connect_str):
    print("Construct called")
    self.connect_str = connect_str
    self.connect()

  def connect(self):
    print("Connecting to DB..")
    engine = create_engine("%s" % (self.connect_str),echo = True)
    engine.connect()
