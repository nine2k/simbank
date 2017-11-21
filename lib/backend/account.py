class Account():
  """ This class stored information associated with
  one account: name, balance, account number
  """

  def __init__(self, number, balance, name):
    self.number = number
    self.balance = balance
    self.name = name

  # implement the rich comparison functions for sorting
  # and equality comparison functions
  def __lt__(self, other):
    return self.number < other.number

  def __gt__(self, other):
    return self.number > other.number

  def __eq__(self, other):
    if (self.number == other.number and \
    self.balance == other.balance and \
    self.name == other.name):
      return True
    else:
      return False

  def __le__(self, other):
    return self.number <= other.number

  def __ge__(self, other):
    return self.number >= other.number

  def __ne__(self, other):
    if (self.number != other.number or \
    self.balance != other.balance or \
    self.name != other.name):
      return True
    else:
      return False

  def deposit(self, amount):
    """ Add amount to current balance
    """
    self.balance += amount

  def withdraw(self, amount):
    """ Deduct amount from current balance
    """
    self.balance -= amount
