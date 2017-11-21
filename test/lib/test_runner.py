import re
import sys
import os
import traceback
from time import time
from shutil import copytree
from test_files import *
from errs import *
from run_helper import *
from test_asserts import *

class TestRunner():
  """ Test runner to execute tests and file report
  """
  executed = 0
  passed = 0
  failed = 0
  test_records = []
  separator = '----------------------------------'

  def __init__(self):
    """ Get the RunHelper() and set up the test dir  
    """
    self._get_test_dir()
    self.run = RunHelper()

  def run_test(self, test):
    """ Runs the test by importing the test script, then
    clean up after the run. Also keep track of whether the
    test failed or passed, and log the test result
    """
    self.current_test = os.path.abspath(test)
    if (not os.path.isfile(self.current_test)):
      sys.exit("Cannot find test file")
 
    self.current_test_orig_dir = os.path.dirname(self.current_test)
    no_ext = os.path.splitext(self.current_test)[0]
    self._get_current_test_dir()
       
    sys.path.append(self.current_test_dir)
    try:
      print"{}Running: {}\n".format(self.separator, self.current_test_name)
      code =  __import__('testscript')
    except TestFailed as e:
      # If a test failed here it's most likely due to a bug
      self.failed += 1
      self.executed += 1
      report = "failed: {}, reason: {}".format(self.current_test_name, e)
      print(e)
      self.write_traceback(traceback.format_exc())
    except Exception as e:
      # If a test failed here it's most likely due to a test error
      # Print the stacktrace
      self.failed += 1
      self.executed += 1
      report = "failed: {}, error: {}".format(self.current_test_name, e)
      print(e)
      self.write_traceback(traceback.format_exc())
      traceback.print_exc()
    else:
      # Otherwise test passes
      self.passed += 1
      self.executed += 1
      report = "passed: {}".format(self.current_test_name)
    finally:
      # Log the result to the test report
      self.test_records.append(report)
      print("\n{}{}".format(self.separator, report))
      # reset the current test information
      self._reset_current_test()

  def write_traceback(self, tb):
    f = open(self.run.new_file('FAILURE'), 'w')
    f.write(tb)
    f.close()  

  def run_tests(self, tests):
    """ Call run_test for each test in a list
    """
    for test in tests:
      self.run_test(test)

    # At the end, log all results and print the test results
    self.log_results()
    self.get_run_results()    

  def log_results(self):
    """ For each record write it to records.log in the test run
    directory
    """
    results_file = os.path.join(self.test_dir, "results.log")
    f = open(results_file, 'w')

    for line in self.test_records:
      f.write("{}\n".format(line))
    f.close()      

  def get_run_results(self):
    """ Print test results: how many tests executed, passed, failed
    """
    print("Tests executed: {}".format(self.executed))
    print("Tests passed: {}".format(self.passed))
    print("Tests failed: {}".format(self.failed))

  def _reset_current_test(self):
    """ Reset all information about the current test and unimport the
    module
    """
    sys.path.remove(self.current_test_dir)
    sys.modules.pop('testscript', None)
    self.current_test = None
    self.current_test_name = None
    self.current_test_dir = None
    self.current_test_orig_dir = None
    self.run.reset()

  def _get_test_dir(self):
    """ Create a folder called results in the home directory and
    store all test results under directory created using the current
    time. Add a symlink 'latest' to the latest run
    """
    results = os.path.join(os.environ['HOME'], 'results')
    if not os.path.exists(results):
      os.makedirs(results)
    test_dir = os.path.join(results, str(time()).replace('.', ''))    
    os.makedirs(test_dir)
    self.test_dir = test_dir

    latest = os.path.join(results, 'latest') 
    if os.path.exists(latest):
      os.unlink(latest)  
    os.symlink(test_dir, latest)

  def _get_current_test_dir(self):
    """ Set information such as current test dir, current test name etc
    for the test currently running
    """
    current_test_dir = os.path.join(self.test_dir, os.path.basename(self.current_test_orig_dir))
    self.current_test_dir = current_test_dir
    self.current_test_name = re.sub(r"^.+simbank\/test\/", '', self.current_test_orig_dir)
    self.run.set_current_test_dir(current_test_dir)
    copytree(self.current_test_orig_dir, self.current_test_dir)
