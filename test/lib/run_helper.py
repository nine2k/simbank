import os
from errs import *


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class RunHelper():
  """ Singleton class that stores information about the
  current test being ran
  """
  __metaclass__ = Singleton
  current_test_dir = None

  def get_current_test_dir(self):
    """ Return the location of the current test directory
    """
    return self.current_test_dir

  def set_current_test_dir(self, d):
    """ Set the location of the current test directory
    """
    self.current_test_dir = d

  def new_file(self, f):
    """ If a new file is to be created under the current
    test directory, return its would-be path
    """
    new_file = os.path.join(self.current_test_dir, f)
    return new_file

  def assert_get_file(self, f):
    """ Get a file by name from the current test directory
    raise an error if it does not exist
    """
    f = os.path.join(self.current_test_dir, f)
    if (os.path.isfile(f)):
      return f
    else:
      raise TestFailed("File {}  does not exist in the current test dir".format(f))

  def get_current_test_summary(self):
    """ Get the summary file outputted by the current test
    """
    return os.path.join(self.current_test_dir, 'summary.txt')

  def get_current_test_log(self):
    """ Get the test log outputted by the current test
    """
    return os.path.join(self.current_test_dir, 'output.log')

  def get_current_test_expected_summary(self):
    """ Get the expected summary file for the test
    """
    return os.path.join(self.current_test_dir, 'expected_summary.txt')

  def get_current_test_expected_log(self):
    """ Get the expected output log for the test
    """
    return os.path.join(self.current_test_dir, 'expected_output.log')
  
  def reset(self):
    """ Set the current test directory to None at the end of the test
    """
    self.current_test_dir = None
