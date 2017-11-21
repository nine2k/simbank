class Logger():
  """ Static helper class meant to unify the format
  of program outputs
  """

  @classmethod
  def warn(self, msg):
    """ Prints a warning message
    """

    print("WARNING: {}".format(msg))

  @classmethod
  def error(self, msg):
    """ Prints an error message
    """

    print("ERROR: {}".format(msg));
  
  @classmethod
  def ignored_transaction(self, msg):
    """ Prints an message indicating an error
    has been detected by ignored
    """

    print("IGNORED TRANSACTION: {}".format(msg));

  @classmethod
  def completed_transaction(self, msg):
    """ Prints an message indicating a transaction
    has been completed on the backend
    """

    print("COMPLETED TRANSACTION: {}".format(msg));

  @classmethod
  def info(self, msg):
    """ Prints an info message, used for any standard messages
    """

    print("INFO: {}".format(msg));
