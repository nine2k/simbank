from expect_helper import *
from test_files import *
from run_helper import *
from test_asserts import *

p = ExpectHelper()
p.start(TEST_FILE1)
p.login('agent')
p.delete_account('22345678', 'Emily')
p.deposit('22345678', '100')
p.logout()
p.quit()
assert_test_log()
assert_test_summary()
