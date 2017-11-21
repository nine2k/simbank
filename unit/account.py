import sys
sys.path.append('/home/ubuntu/school/cisc327/simbank/lib')

import unittest
import mock
import backend.account
import helpers.logger
import helpers.errors
import backend.account_manager

class TestAccount(unittest.TestCase):

    def test_deduct_amount(self):
      act = backend.account_manager.Account(11111112, 100100, 'Emma Chen')
      act.withdraw(100)
      self.assertEqual(act.balance, 100000)


if __name__ == '__main__':
    unittest.main()
