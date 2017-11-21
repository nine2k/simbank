from errs import *
from run_helper import *
import filecmp
import os
import sys


def assert_test_log():
  """ Strip all lines of expected output log and test generated output log
  and compare them to see if they are the same or different.
  If they are the same, then the assertion passes otherwise raise and error
  """
  expected_log = RunHelper().get_current_test_expected_log()
  test_log = RunHelper().get_current_test_log()

  if (not os.path.isfile(expected_log)):
    raise TestFailed("Expected log does not exist")

  if (not os.path.isfile(test_log)):
    raise TestFailed("Test log was not generated")

  test  = [str.strip(line) for line in open(test_log, 'r').readlines()]
  expected = [str.strip(line) for line in open(expected_log, 'r').readlines()]

  if (''.join(expected) != ''.join(test)): 
    raise TestFailed("Test log does not match expected log")


def assert_test_summary():
  """ Strip all lines of expected transaction summary and test generated transaction
  summary and compare them to see if they are the same or different.
  If they are the same, then the assertion passes otherwise raise and error
  """
  expected_summary = RunHelper().get_current_test_expected_summary()
  test_summary = RunHelper().get_current_test_summary()

  if (not os.path.isfile(expected_summary)):
    raise TestFailed("Expected summary file does not exist")

  if (not os.path.isfile(test_summary)):
    raise TestFailed("Test summary file was not generated")

  test  = [str.strip(line) for line in open(test_summary, 'r').readlines()]
  expected = [str.strip(line) for line in open(expected_summary, 'r').readlines()]

  if (''.join(expected) != ''.join(test)):    
    raise TestFailed("Test summary file does match expected summary")
