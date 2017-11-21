from logger import *
from errors import ProgramTermination

class InputValidator():
  """ This class validates the command and normalizes the format
  If the command is not valid, an error is raised and SimBank catches the
  error and prompts the user to enter another command until successful
  """


  @classmethod
  def validate_command(self, cmd):
    """ Checks and verifies command
    """  
     
    cmd = cmd.split()
    cmd[0] = cmd[0].lower()
    single_account_transaction = ["withdraw", "deposit"]
    two_accounts_transaction = ["transfer"]
    account_manage = ["create", "delete"]
    valid_commands = single_account_transaction + two_accounts_transaction + account_manage

    if (cmd == ["login"] or cmd == ["logout"]):
      return cmd[0]
    elif (cmd[0] == "quit"):
      raise ProgramTermination()
    elif (cmd[0] in valid_commands):
      if (cmd[0] in single_account_transaction):
        cmd = self.check_cmd_length(cmd, 3)
        cmd[1] = self.normalize_account_format(cmd[1])
        cmd[2] = self.normalize_amount_format(cmd[2])
      elif (cmd[0] in two_accounts_transaction):
        cmd = self.check_cmd_length(cmd, 4)
        cmd[1] = self.normalize_account_format(cmd[1])
        cmd[2] = self.normalize_account_format(cmd[2])
        cmd[3] = self.normalize_amount_format(cmd[3])
      elif (cmd[0] in account_manage):
        cmd = self.check_cmd_length_gte(cmd, 3)
        cmd[1] = self.normalize_account_format(cmd[1])
        cmd[2] = self.normalize_name_format(cmd[2:])
      return cmd
    else:
      raise ValueError("Invalid command")
  

  @classmethod
  def check_cmd_length(self, cmd, length):
    """ Checks the length of commands, if it does not have the 
    expected length function throws error message
    """
      
    if (len(cmd) != length):
      raise ValueError("Invalid command format")

    return cmd
  
  @classmethod
  def check_cmd_length_gte(self, cmd, length):
    """ Checks the length of commands, if it does not have the 
    expected length function throws error message
    """
      
    if (len(cmd) < length):
      raise ValueError("Invalid command format")
    return cmd 
 
  @classmethod
  def normalize_account_format(self, account):
    """ Checks and verifies account, if it is not a valid account number
    function throws error message. Return the account in integer form
    """
      
    if (not self.is_valid_account_number(account)):
      raise ValueError("Invalid account number {}".format(account))
    else:
      return int(account)


  @classmethod
  def normalize_amount_format(self, amount):
    """ Checks and verifies amount, if it is not a valid transaction amount
    function throws error message. Return the amount in integer form
    """
      
    if (not self.is_valid_num(amount)):
      raise ValueError("Invalid transaction amount {}".format(amount))
    else:
      return int(amount)


  @classmethod
  def normalize_name_format(self, name):
    """ Checks for validity of account name, if it is not a valid account name
    function throws error message. Return a name with each of the first letter
    capitalized.
    """

    name = " ".join(name)
      
    if (not self.is_valid_account_name(name)): 
      raise ValueError("Invalid account name {}".format(name))
    else:
      return name.title()


  @classmethod
  def is_valid_num(self, num):
    """ Checks if input is all digits
    """
      
    if num.isdigit():
      return True
    return False


  @classmethod  
  def is_valid_account_name(self, value):
    """ Checks if value is less than 30 alphanumeric characters
    """

    if (value.replace(' ', '').isalnum() and 30 >= len(value) >= 3):
      
      return True
    return False


  @classmethod
  def is_valid_account_number(self, num):
    """ Check format and length of account number
    """
      
    if (num == "00000000" or num.startswith("0")):
      return False
    elif (len(num) == 8 and num.isdigit()):
      return True
    else:
      return False

  @classmethod
  def is_valid_master_account_file_line(self, line):
    """ Checks the length of a line in the master account
    file
    """
  
    if (len(line) > 48):
      raise ValueError("A line in the master accounts file is longer than 48 characters")
    return True
