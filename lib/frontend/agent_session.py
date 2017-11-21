from session import Session
from summary import *

class AgentSession(Session):
  """ AgentSession class is a child class of the abstract class "Session"
  It allows the user to perform privileged bank transactions - deposit,
  withdraw, transfer, create account and delete account
  It also verfies input looking for constraints and value error (invalid amount)
  """ 

  _new_accounts = []
  _deleted_accounts = []
  

  def deposit(self, account, amount):
    """ Checks amount and makes deposit to account
    """

    if (0 <= amount <= 99999999):
      self.summary.record_deposit(account, amount)
    else:
      raise ValueError("Invalid transaction value for agent mode")


  def withdraw(self, account, amount):
    """ Checks amount and withdraws from account
    """

    if (0 <= amount <= 99999999):
      self.summary.record_withdraw(account, amount)
    else:
      raise ValueError("Invalid transaction value for agent mode")


  def transfer(self, account1, account2, amount):
    """ Checks amount and makes transfer
    """

    if (0 <= amount <= 99999999):
      self.summary.record_transfer(account1, account2, amount)
    else:
      raise ValueError("Invalid transaction value for agent mode")


  def is_account_new(self, account):
    """ Check if the account is a new account created in this session
    """
    
    if (account in self._new_accounts):
      return True
    else:
      return False


  def create_account(self, account, name):
    """ Creates account
    """
 
    if (not (self.accounts.is_account_active(account) or self.is_account_new(account))):
      self._new_accounts.append(int(account))
      self.summary.record_create_account(account, name)
    else:
      raise ValueError("Account {} already exists".format(account))


  def delete_account(self, account, name):
    """ Delete account, remove account from active accounts in accounts and 
    add it to the _deleted_accounts list
    """    

    if (self.accounts.is_account_active(account)):
      self.accounts.delete_account(account)
      self._deleted_accounts.append(account)
      self.summary.record_delete_account(account, name)
    else:
      raise ValueError("Account {} is not active, it cannot be deleted".format(account))
