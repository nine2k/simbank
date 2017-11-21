from helpers.input_validator import *
from helpers.logger import *
from helpers.errors import *
from backend.account import *
import sys

class AccountManager():
  """ Class that keeps and manages a list of accounts
  and their balances and processes the transactions
  """

  def __init__(self):
    """ Instantiates
    """
    self.account_list = []

  def account_create(self, number, name):
    """ Add a new account into the account list
    """
    try:
      account = self.get_account_by_number(number)
    except AccountNotFound as e: 
      # create the account is AccountNotFound is raised
      self.account_list.append(Account(number, 0, name))
      sorted(self.account_list)
      Logger.completed_transaction("Created account {} with name {}".format(number, name))
    else:
      raise BackendConstraintError("Account {} cannot be added as account number already exists".format(number))

  def account_delete(self, number, name):
    """ Remove an account from the account list
    """
    account = self.get_account_by_number(number)
    if (account.balance == 0):
      # match the name
      if (account.name.lower() == name.lower()):
        self.account_list.remove(account)
        Logger.completed_transaction("Deleted account {} with name {}".format(number, name))
      else:
        raise BackendConstraintError("Name {} does not match account {}'s name {}".format(name, account.number, account.name))
    else:
      raise BackendConstraintError("Account {} cannot be deleted as it does not have a balance of 0".format(account.number))

  def account_withdraw(self, number, amount):
    """ Withdraw an amount from the account
    """
    account = self.get_account_by_number(number)
    if (account.balance - amount < 0):
      raise BackendConstraintError("A transaction resulted in a negative balance for account {}".format(account.number))
    else:
      account.withdraw(amount)
      Logger.completed_transaction("Withdraw amount {} from account {}".format(amount, number))

  def account_deposit(self, number, amount):
    """ Deposit an amount from the account
    """
    account = self.get_account_by_number(number)
    if (account.balance + amount < 0):
      raise BackendConstraintError("A transaction resulted in a negative balance for account {}".format(account.number))
    else:
      account.deposit(amount)
      Logger.completed_transaction("Deposit amount {} to account {}".format(amount, number))

  def account_transfer(self, number_to, number_from, amount):
    """ Withdraw an amount from number_from and deposit
    into number_to
    """
    account_to = self.get_account_by_number(number_to)
    account_from = self.get_account_by_number(number_from)
    if (account_to.balance + amount < 0):
      raise BackendConstraintError("A transaction resulted in a negative balance for account {}".format(account_to.number))
    elif (account_from.balance - amount < 0):
      raise BackendConstraintError("A transaction resulted in a negative balance for account {}".format(account_from.number))
    else:
      account_to.deposit(amount)
      account_from.withdraw(amount)
      Logger.completed_transaction("Transfer from account {} to {} amount {}".format(number_from, number_to, amount))

  def get_account_by_number(self, number):
    """ Return an account object by its account number
    """

    for account in self.account_list:
      if (account.number == number):
        return account
    
    raise AccountNotFound("Account {} is not found".format(number))
