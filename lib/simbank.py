import os.path
import sys
from sys import argv
from frontend.accounts import *
from frontend.session import *
from helpers.logger import *
from helpers.input_validator import *
from helpers.errors import *
from frontend.agent_session import *
from frontend.atm_session import *

class SimBank:
  """ This is the main class of simbank where the program is ran and 
  commands are processed
  """  

  accounts = Accounts()

  def __init__(self, args):

    # first check the commandline arguments
    (account_file,output_file) = self.check_arguments(args)
    # read the accounts from the first commandline argument
    self.accounts.read_accounts_from_file(account_file)
    # store the path of the output file for later use
    self.output_file = output_file

    # in the beginning, logged in status is False and self.mode
    # is None
    self.logged_in = False
    self.mode = None


  def check_arguments(self, args):
    """ Checks the commandline arguments provided by the user
    if there are more than 1 arguments provided, only use the first one
    """

    if (len(args) <= 2):
      Logger.error("An input file and an output file are needed to run the program")
      exit(1)
    else:
      if (len(args) > 3):
        Logger.error("Too many arguments")
        exit(1)
      if (os.path.isfile(args[1])):
        return (args[1], args[2])
      else:
        Logger.error("File {} does not exist".format(args[1]))
        exit(1)


  def get_next_command(self):
    """ Prompt the user to enter a command
    """

    cmd = raw_input("Enter a command: ")
    return cmd


  def login(self):
    """ If the user is not currently logged in, prompt the user to select
    a mode or logout. If the user selects atm, initialize an ATM instance,
    if the user selects agent, initialize an Agent instance. The user can
    also choose to logout to abort the session.
    """

    # Login is valid if self.mode is not set
    while self.mode is None:
      mode_input = raw_input("Select mode (atm/agent) or logout: ")
      if (mode_input.lower() == "atm"):
        # initiate an ATMSession() and set logged in status to True
        self.mode = ATMSession()
        self.logged_in = True
        Logger.info("Logged into atm mode")
      elif (mode_input.lower() == "agent"):
        # initiate an AgentSession() and set logged in status to True
        self.mode = AgentSession()
        self.logged_in = True
        Logger.info("Logged into agent mode")
      elif (mode_input.lower() == "logout"):
        # also accept logging out as an option from this stage
        self.logout()
        break
      else:
        Logger.error("Invalid mode {}".format(mode_input))
  
 
  def logout(self):
    """ End the session and set self.mode to None
    """

    # set logged in status to False
    self.logged_in = False
    if (self.mode is not None):
      # end the session, which triggers writing transaction summaries
      # to an output file
      self.mode.end_session(self.output_file)
      self.mode = None
 
    Logger.info("Logged out")

  def process_command(self, cmd):
    """ Process the command and delegate to other functions
    """

    if (not self.logged_in):
      if (cmd != "login"):
        Logger.error("Cannot process command before login")
      else:
        self.login()
    else:
      if (cmd == "login"):
        Logger.error("Already logged in")
      elif (cmd == "logout"):
        self.logout()
      elif (cmd[0] == "withdraw"):
        self.process_withdraw(cmd)
      elif (cmd[0] == "deposit"):
        self.process_deposit(cmd)
      elif (cmd[0] == "transfer"):
        self.process_transfer(cmd)
      elif (cmd[0] == "create"):
        self.process_create_account(cmd);
      elif (cmd[0] == "delete"):
        self.process_delete_account(cmd);


  def process_withdraw(self, cmd):
    """ Parse the command, check the validity of the account, and process the transaction: withdraw
    """

    account = cmd[1]
    amount = cmd[2]
    
    if (self.accounts.is_account_active(account)):
      self.mode.withdraw(account, amount)
    else:
      raise ValueError("Account {} does not exist or is currently inactive".format(account))
    
    Logger.info("Withdraw complete: {} from account {}".format(amount, account))

  def process_deposit(self, cmd):
    """ Parse the command, check the validity of the account, and process the transaction: deposit
    """

    account = cmd[1]
    amount = cmd[2]

    if (self.accounts.is_account_active(account)):
      self.mode.deposit(account, amount)
    else:
      raise ValueError("Account {} does not exist or is currently inactive".format(account))
    
    Logger.info("Deposit complete: {} to account {}".format(amount, account))
  
 
  def process_transfer(self, cmd):
    """ Parse the command, check the validity of the accounts, and process the transaction: transfer
    """

    account1 = cmd[1]
    account2 = cmd[2]
    amount = cmd[3]
   
    if (not self.accounts.is_account_active(account1)):
      raise ValueError("Account {} does not exist or is currently inactive".format(account1))
    elif (not self.accounts.is_account_active(account2)):
      raise ValueError("Account {} does not exist or is currently inactive".format(account2))
    else:    
      self.mode.transfer(account1, account2, amount) 
    
    Logger.info("Transfer complete: {} from account {} to account {}".format(amount, account1, account2))

  def process_create_account(self, cmd):
    """ Create a new account
    """
    account = cmd[1]
    name = cmd[2]

    self.mode.create_account(account, name) 

    Logger.info("Create account complete: name {} account number {}".format(name, account))

  def process_delete_account(self, cmd):
    """ Delete an account
    """

    account = cmd[1]
    name = cmd[2]
    
    self.mode.delete_account(account, name) 
    
    Logger.info("Delete account complete: name {} account number {}".format(name, account))

  
  def simbank_run(self):
    """ Main function to run the program, every iteration prompts for a command, check that the command is in
    a valid format, if it is, then process the command
    """

    while True:
      try:
        # continutously prompt for next command
        cmd = self.get_next_command()
        # normalize and validate each command
        cmd = InputValidator.validate_command(cmd)
        # take actions for a valid command
        self.process_command(cmd)
      except (ValueError, PrivilegeError) as e:
        Logger.error(e)
      except (KeyboardInterrupt, ProgramTermination):
        # quit the program if there's a KeyboardIntterup or the program
        # catches ProgramTermination
        print("")
        exit(0)




# Runs the program by initializing the class with the commandline
# arguments and calling simbank_run()
if __name__ == '__main__':
  main = SimBank(argv)
  main.simbank_run()
