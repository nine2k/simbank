import sys
from sys import argv
from helpers.logger import *
from helpers.input_validator import *
from helpers.errors import *
from backend.account_manager import *
from backend.account import *

class SimBankBackOffice():

  def __init__(self, args):
    self.master_accounts_file = args[1]
    self.transaction_summary = args[2]
    self.new_master_accounts_file = args[3]
    self.new_accounts_file = args[4]
    self.accounts = AccountManager()
    self.read_master_accounts_file()


  def read_transaction_summary(self):
    """ Read the a treansaction file from path
    """
    summary = []
    try:
      f = open(self.transaction_summary)
      lines = f.readlines()
      f.close()
    except IOError as e:
      Logger.error(e)
      sys.exit(1)
    else:
      for s in lines:
        if (s.strip() != ''):
          summary.append(s.strip())

      return summary

  def read_master_accounts_file(self):
    """ Reads in a master accounts file and store each account
    in an Account object
    """
    try:
      f = open(self.master_accounts_file);
      lines = f.readlines()
      f.close()
    except IOError as e:
      Logger.error(e)
      sys.exit(1)
    else:
      for line in lines:
        if (InputValidator.is_valid_master_account_file_line(line)):
          line = line.strip()
          line = line.split()
          # get the number, balance and name from the line
          number = InputValidator.normalize_account_format(line[0])
          balance = InputValidator.normalize_amount_format(line[1])
          name = InputValidator.normalize_name_format(line[2:])

          # create an account object and add it to the list
          self.accounts.account_list.append(Account(number, balance, name))

      # sort the accounts
      sorted(self.accounts.account_list)

  def write_master_accounts_file(self):
    """ Writes to the new account file with the current accounts
    """
    f = open(self.new_master_accounts_file, 'w')

    for account in self.accounts.account_list:
      line = "{} {:03d} {}\n".format(account.number, account.balance, account.name)
      if (InputValidator.is_valid_master_account_file_line(line)):
        f.write(line)
    f.close()

  def write_accounts_file(self):
    """ Writes to the new account file with the current accounts
    """
    f = open(self.new_accounts_file, 'w')

    for account in self.accounts.account_list:
      line = "{}\n".format(account.number)
      f.write(line)
    f.write('00000000')
    f.close()

  def start_backend_processing(self):
    """ Main function to start processing backend transactions
    """
    try:
      summary = self.read_transaction_summary()
      self.process_transaction_summary(summary)
      self.write_master_accounts_file()
      self.write_accounts_file()
      Logger.info("Transactions completed")
      sys.exit(0)
    except ValueError as e:
      Logger.error(e)
      sys.exit(1)
      

  def process_transaction_summary(self, summary):
    """ For each line in the transaction, parse and process
    the transaction on the line
    """
    for line in summary:
      cmd = line.split()
      transaction = cmd[0].strip().lower()
      if (transaction == 'es'):
        break
      else:
        # the first account may be 00000000
        if (cmd[1].strip() != '00000000'):
          account1 = InputValidator.normalize_account_format(cmd[1].strip())
        else:
          account1 = 0
        
        # the second account may be 00000000
        if (cmd[2].strip() != '00000000'):
          account2 = InputValidator.normalize_account_format(cmd[2].strip())
        else:
          account2 = 0
        
        # parse the amount
        amount = InputValidator.normalize_amount_format(cmd[3].strip())
        
        # the account name may be ***
        if (cmd[4] == '***'):
          name = '***'
        else:
          name = InputValidator.normalize_name_format(cmd[4:])
          name = name.strip()
          
        self.process_transaction(transaction, account1, account2, amount, name)

  def process_transaction(self, cmd, account1, account2, amount, name):
    """ processes a transaction
    """
    try:
      if (cmd == 'cr'):
        self.accounts.account_create(account1, name)
      elif (cmd == 'dl'):
        self.accounts.account_delete(account1, name)
      elif (cmd == 'wd'):
        self.accounts.account_withdraw(account1, amount)
      elif (cmd == 'de'):
        self.accounts.account_deposit(account1, amount)
      elif (cmd == 'tr'):
        self.accounts.account_transfer(account1, account2, amount)
    except (BackendConstraintError, AccountNotFound) as e:
      # pass
      Logger.ignored_transaction(e)
    self.accounts.account_list = sorted(self.accounts.account_list)

if (__name__ == '__main__'):
  b = SimBankBackOffice(sys.argv)
  b.start_backend_processing()
