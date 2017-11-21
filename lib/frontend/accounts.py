from helpers.logger import *
from helpers.input_validator import *

class Accounts():
  """ A singleton class that stores all accounts from the valid accounts file
  and maintains a list of active accounts - accounts currently active from the
  accounts file.
  """  

  _active_accounts = []
  _instance = None

  def __new__(self, *args, **kwargs):
    if not self._instance:
      self._instance = super(Accounts, self).__new__(
      self, *args, **kwargs)

    return self._instance


  def is_account_active(self, account):
    """ Checks if account is active
    """

    if (account in self._active_accounts):
      return True
    else:
      return False

  def delete_account(self, account):
    """ Delete the account from _active_accounts
    """
    self._active_accounts.remove(account)

  def read_accounts_from_file(self, file):
    """ Read in accounts from file
    """
    
    f = open(file)
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    for line in lines:
      if (line == '00000000'):
        break
      elif (InputValidator.is_valid_account_number(line)):
        if (not self.is_account_active(line)):
          self._active_accounts.append(int(line))
      else:
        Logger.error("Invalid input file")
        exit(1)
