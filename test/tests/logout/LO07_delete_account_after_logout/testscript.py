from expect_helper import *
from test_files import *
from run_helper import *
from test_asserts import *


p = ExpectHelper()
p.start(TEST_FILE1)
p.login('atm')
p.logout()
p.delete_account('12345678', 'John')
p.quit()

assert_test_log()
assert_test_summary()
