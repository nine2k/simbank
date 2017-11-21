import sys
sys.path.append('/home/ubuntu/school/cisc327/simbank/lib')

import unittest
import mock
import backend.account
import helpers.logger
import helpers.errors
import backend.account_manager


def mock_get_account_by_number(obj, number):
  return backend.account.Account(11111112, 10000, 'Emma Chen')

def mock_logger_completed_transaction(msg):
  pass
    
class TestAccountWithdraw(unittest.TestCase):
    tc = 0

    @mock.patch('backend.account_manager.AccountManager.get_account_by_number', mock_get_account_by_number)
    def test_negative_balance_error(self):
      mgr = backend.account_manager.AccountManager()
      with self.assertRaises(helpers.errors.BackendConstraintError):
        mgr.account_withdraw(11111112, 10100)     

    @mock.patch('backend.account_manager.AccountManager.get_account_by_number', mock_get_account_by_number)
    @mock.patch('helpers.logger.Logger.completed_transaction', side_effect=mock_logger_completed_transaction)
    def test_withdraw_success(self, m1):
      
      mgr = backend.account_manager.AccountManager()
      mgr.account_withdraw(11111112, 100)
      m1.assert_called_once_with('Withdraw amount 100 from account 11111112') 
  
    @mock.patch('helpers.logger.Logger.completed_transaction', side_effect=mock_logger_completed_transaction)
    def test_check_active_account(self, m1):
      mgr = backend.account_manager.AccountManager()
      mgr.account_list.append(backend.account.Account(11111112, 10100, 'Emma Chen'))
      mgr.account_withdraw(11111112, 10100)
      m1.assert_called_once_with('Withdraw amount 10100 from account 11111112') 
      
    
    def test_check_inactive_account(self):
      mgr = backend.account_manager.AccountManager()
      with self.assertRaises(helpers.errors.AccountNotFound):
        mgr.account_withdraw(11111112, 10100)

if __name__ == '__main__':
    global tc
    unittest.main()
