from expect_helper import *
from test_files import *
from run_helper import *
from test_asserts import *

p = ExpectHelper()
p.start(TEST_FILE1)
p.login('atm')
p.deposit('12345678','90000')
p.deposit('12345678','10100')
p.logout()
p.quit()
assert_test_log()
assert_test_summary()
