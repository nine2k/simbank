from expect_helper import *
from test_files import *
from run_helper import *
from test_asserts import *

p = ExpectHelper()
p.start(TEST_FILE1)
p.login('agent')
p.withdraw('12345678','100100')
p.logout()
p.quit()
assert_test_log()
