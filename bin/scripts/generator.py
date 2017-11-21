# this is a script that generates program input automatically
# input commands are generated based on existing information for
# a set of accounts

from random import randint
import names
import time
import sys

def generate_random_name():
  return names.get_full_name()

def generate_random_transaction(accounts, session):
  ''' randomly generate one of the transactions
  '''
  transactions = ['withdraw', 'deposit', 'transfer', 'create', 'delete']
  
  if (session == 'agent'):
    rand = randint(0, len(transactions) - 1)
  else:
    # atm mode cannot create or delete
    rand = randint(0, len(transactions) - 3)
  
  if (rand == 0):
    return generate_withdraw(accounts, session)
  elif (rand == 1):
    return generate_deposit(accounts, session)
  elif (rand == 2):
    return generate_transfer(accounts, session)
  elif(rand == 3):
    return generate_create(accounts)
  else:
    return generate_delete(accounts)

def generate_session():
  ''' choose between an atm session or an agent session
  '''
  modes = ['atm', 'agent']
  rand = randint(0, len(modes) - 1)
  return modes[rand]

def generate_deposit(accounts, session):
  # choose account to deposit to
  rand = randint(0, len(accounts) - 1)
  if (session == 'agent'):
    amount = randint(0, 100000000)
  else:
    amount = randint(0, 100001)

  return (accounts, 'deposit {} {}'.format(accounts.keys()[rand], amount))

def generate_withdraw(accounts, session):
  ''' produce a withdraw command from an account
  the withdraw amount cannot be more than their balance
  and cannot exceed the limit for modes 
  '''
  rand = randint(0, len(accounts) - 1)
  account = accounts.keys()[rand]
  balance = accounts[account][0]
  if (balance == 0):
    return (account, '')

  amount = randint(1, balance+1)
  if (session == 'agent'):
    while (amount > 100000000):
      amount = randint(1, balance)
  else:
    while (amount > 100001):
      amount = randint(1, balance)
  
  return (accounts, 'withdraw {} {}'.format(account, balance))

def generate_transfer(accounts, session):
  ''' produce a transfer command from an account to another
  the transfer amount cannot be more than their balance
  and cannot exceed the limit for modes 
  '''
  if (len(accounts) < 2):
    return (account, '')
  rand1 = randint(0, len(accounts) - 1)
  rand2 = randint(0, len(accounts) - 1)
  while (rand2 == rand1):
    rand2 = randint(0, len(accounts) - 1)
    
  account_from = accounts.keys()[rand1]
  account_to = accounts.keys()[rand2]
  balance = accounts[account_from][0]
  if (balance == 0):
    return (accounts, '')
  
  amount = randint(1, balance)
  if (session == 'agent'):
    while (amount > 100000000):
      amount = randint(1, balance)
  else:
    while (amount > 100001):
      amount = randint(1, balance)
  
  return (accounts, 'transfer {} {} {}'.format(account_from, account_to, amount))

def generate_create(accounts):
  ''' generate command to create an account
  '''
  account = randint(10000000, 99999999)
  while (account in accounts.keys()):
    account = randint(10000000, 99999999)
  
  name = generate_random_name()  
  accounts[account] = (0, name)

  return (accounts, 'create {} {}'.format(account, name))

def generate_delete(accounts):
  ''' generate command to delete an account
  '''
  for key, value in accounts.iteritems():
    if (value[0] == 0):
      return (accounts, 'delete {} {}'.format(key, value[1]))

  return (accounts, '')

def generate_session_transactions(accounts, session):
  ''' generate anywehere between 5 and 10 transactions for a
  session
  '''
  transactions = []

  num = randint(5, 10)
  while (num > 0):
    (a, cmd) = generate_random_transaction(accounts, session)
    if (cmd != ''):
      transactions.append(cmd)
      num = num - 1

  return transactions

def create_transaction_file(accounts):
  ''' generate the complete input file for running the program
  '''
  filename = "tran_{}".format(int(round(time.time() * 1000)))
  transactions = ['login']
  session = generate_session()
  transactions.append(session)

  transactions += generate_session_transactions(accounts, session)
  transactions.append('logout')
  transactions.append('quit')
  f = open(filename, 'w')
  for t in transactions:
    if (t.strip() != ''):
      f.write('{}\n'.format(t.strip()))

  f.close()
  print("### created transaction file {} ###".format(filename))
  return filename

def create_accounts_session():
  ''' generate a session where only accounts are created, used for
  running the first session
  '''
  accounts = {}
  transactions = ['login', 'agent']
  filename = "tran_{}".format(int(round(time.time() * 1000)))
  num = randint(10,15)

  while (num > 0):
    (accounts, cmd) = generate_create(accounts)
    transactions.append(cmd)
    num = num - 1

  transactions += ['logout', 'quit']
  
  f = open(filename, 'w')
  for line in transactions:
    if (line.strip() != ''):
      f.write("{}\n".format(line))

  f.close()
  print("### created transaction file {} ###".format(filename))
  return filename
