import pexpect
import sys
import os
from run_helper import *
from errs import *

class ExpectHelper():
  """ Helper to expect and send commands to the simbank program
  It uses the pexpect module to handle expect and send
  """

  COMMAND_PROMPT = 'Enter a command: '
  LOGIN_PROMPT = 'Select mode \(atm\/agent\) or logout: '

  def __init__(self):
    self.timeout = 1
    

  def set_timeout(self, timeout):
    """ Set the timeout for pexpect
    """
    self.timeout = timeout

  def spawn(self, infile="", outfile=""):
    """ Spawn a program using infile and outfile, by default outfile gets set
    to a specific name defined by RunHelper().get_current_test_summary()
    """
    p = pexpect.spawn("simbank {} {}".format(infile, RunHelper().get_current_test_summary()))
     
    # All log files are recorded in a file specified by 
    # RunHelper().get_current_test_log()
    fout = file(RunHelper().get_current_test_log(), 'w')
    p.logfile_read = fout
    self.spawn = p

  def expect(self, expect, terminate=False):
    """ Expect a message and terminate the process if terminate
    is set to True
    """
    try:
      self.spawn.expect(expect)
    except pexpect.ExceptionPexpect as e:
      print(e)
      raise TestFailed("Pexpect existed unexpectedly") 
      
    if (terminate):
      self.terminate()
      print('\nProgram terminated by force')

  def expect_send(self, expect, send, t=None):
    """ Expect a message and send a message, set the timeout using
    t if needed, but t defaults to default self.timeout value
    """
    if (self.spawn is None):
      sys.exit("No process has been spawned")

    if (t is None):
      t = self.timeout

    try:
      self.spawn.expect(expect, timeout=t)
      self.spawn.sendline(send)
    except pexpect.ExceptionPexpect as e:
      print(e)
      raise TestFailed("Pexpect existed unexpectedly")
  
  def expect_error(self, terminate=True):
    """ Indicate that an error is expected and terminate
    the program
    """
    self.expect("ERROR: .+", terminate)
  
  def start(self, infile="", outfile=""):
    """ Start the program with infile and outfile
    """
    self.spawn(infile, outfile)

  def login(self, mode=None):
    """ Login to a mode if mode is specified, otherwise
    just enter the login command
    """
    self.expect_send(self.COMMAND_PROMPT, "login")
    if (not mode is None):
      self.expect_send(self.LOGIN_PROMPT, mode)
  
  def withdraw(self, account, amount):
    """ Send a withdraw command to the program
    """
    self.expect_send(self.COMMAND_PROMPT, "withdraw {} {}".format(account, amount))

  def deposit(self, account, amount):
    """ Send a deposit command to the program
    """
    self.expect_send(self.COMMAND_PROMPT, "deposit {} {}".format(account, amount))

  def transfer(self, account1, account2, amount):
    """ Send a transfer command to the program
    """
    self.expect_send(self.COMMAND_PROMPT, "transfer {} {} {}".format(account1, account2, amount)) 

  def create_account(self, account, name):
    """ Send a create anccount command to the program
    """
    self.expect_send(self.COMMAND_PROMPT, "create {} {}".format(account, name))

  def delete_account(self, account, name):
    """ Send a delete account command to the program
    """
    self.expect_send(self.COMMAND_PROMPT, "delete {} {}".format(account, name))

  def logout(self):
    """ Send a logout command to the program
    """
    self.expect_send(self.COMMAND_PROMPT, "logout") 

  def quit(self):
    """ Send a quit command to the program
    """
    self.expect_send(r'({}|{})'.format(self.COMMAND_PROMPT, self.LOGIN_PROMPT),"quit")
    self.terminate()
    print("quit")
    print("Program exited by command.")

  def terminate(self):
    """ Terminate the pexpect spawn process and copy whatever
    is in the log file to a file specified by RunHelper().get_current_test_log()
    """
    f = open(RunHelper().get_current_test_log(), 'r')
    for line in f.readlines():
      sys.stdout.write(line)
    print('')
    f.close()    
    self.spawn.close(0)
   
