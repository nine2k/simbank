from session import Session
from helpers.errors import *

    
class ATMSession(Session):
  """ ATMSession class is a child class of the abstract class "Session"
  It allows the user to perform unprivileged bank transactions - deposit,
  withdraw and transfer
  It also verfies input looking for constraints and value error (invalid amount)
  """ 
  
  withdraw_history = {}

  def deposit(self, account, amount):
    """ Checks amount and makes deposit to account
    """
    if (0 <= amount <= 100000):
      self.summary.record_deposit(account, amount)
    else:
      raise ValueError("Invalid transaction value for atm mode")


  def withdraw(self, account, amount):
    """ Checks session withdraw limit remaining
    makes sure withdraw amount is smaller than or equal to limit remaining
    and withdraws from account
    """
    limit_remaining = self.get_limit_remaining(account)

    if (0 <= amount <= 100000):
      if (amount <= limit_remaining):
        self.summary.record_withdraw(account, amount)
        self.withdraw_history[account] = self.withdraw_history[account] + amount
      else:
        raise ValueError("Amount exceed withdraw allowance for account {}".format(account))
    else:
      raise ValueError("Invalid transaction value for atm mode")


  def transfer(self, account1, account2, amount):
    """ Checks amount transferring is valid and within limit remaining
    and makes the transfer
    """
    limit_remaining = self.get_limit_remaining(account1)
    
    if (0 <= amount <= 100000):
      if (amount <= limit_remaining):
        self.summary.record_transfer(account1, account2, amount)
        self.withdraw_history[account1] = self.withdraw_history[account1] + amount
      else:
        raise ValueError("Amount exceed withdraw allowance for account {}".format(account1))
    else:
      raise ValueError("Invalid transaction value for atm mode")


  def create_account(self, account, name):
    """ Raise a Privilege error if the action is attempted
    """

    raise PrivilegeError("Action not allowed in mode atm")


  def delete_account(self, account, name):
    """ Raise a Privilege error if the action is attempted
    """

    raise PrivilegeError("Action not allowed in mode atm")
  

  def get_limit_remaining(self, account):
    """ Checks the limit remaining that users can withdraw from account
    in this session
    """
    if (not (account in self.withdraw_history.keys())):
      self.withdraw_history[account] = 0
   
    return 100000 - self.withdraw_history[account]
