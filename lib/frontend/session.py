from abc import ABCMeta, abstractmethod
from summary import *
from accounts import *

class Session():
  """ Abstract class for performing transactions in a session
  """

  __metaclass__ = ABCMeta

  summary = Summary()
  accounts = Accounts()
 
 
  @abstractmethod
  def deposit(self, account, amount):
    raise NotImplementedError


  @abstractmethod
  def withdraw(self, account, amount):
    raise NotImplementedError


  @abstractmethod
  def transfer(self, account1, account2, amount):
    raise NotImplementedError
  

  @abstractmethod
  def create_account(self, account, name):
    raise NotImplementedError
  

  @abstractmethod
  def delete_account(self, account, name):
    raise NotImplementedError
  

  def end_session(self, output_file):
    """ Record the end of the session and write the summary
    file to output_file
    """
    
    self.summary.record_end_session()

    with open(output_file, "w") as output:
      for transaction in self.summary.records:
        output.write("{}\n".format(transaction))
