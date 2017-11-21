class Summary():
    """ Contains the transaction summaries and record different
    transactions in the approperiate format
    """

    
    def __init__(self):
      self.records = []
    

    def record_create_account(self, account_number, name):
      """ record the create account transaction
      """
  
      self.records.append("CR {:08d} 00000000 000 {}".format(account_number, name))

    def record_delete_account(self, account_number, name):
      """ record the delete account transaction
      """
  
      self.records.append("DL {:08d} 00000000 000 {}".format(account_number, name))

    def record_deposit(self, account_number, amount):
      """ record the deposit transaction
      """
  
      self.records.append("DE {:08d} 00000000 {:03d} ***".format(account_number, amount))

    def record_withdraw(self, account_number, amount):
      """ record the withdraw transaction
      """
  
      self.records.append("WD {:08d} 00000000 {:03d} ***".format(account_number, amount))
    
    def record_transfer(self, from_account, to_account, amount):
      """ record the transfer transaction
      """
  
      self.records.append("TR {:08d} {:08d} {:03d} ***".format(to_account, from_account, amount))

    def record_end_session(self):
      """ record the end of session transaction
      """
  
      self.records.append("ES 00000000 00000000 000 ***")
