from expect_helper import *
from test_files import *
from run_helper import *
from test_asserts import *


p = ExpectHelper()
p.start(TEST_FILE1)
p.login('agent')
p.create_account('07654321', "John")
p.logout()
p.quit()

assert_test_log()
assert_test_summary()
