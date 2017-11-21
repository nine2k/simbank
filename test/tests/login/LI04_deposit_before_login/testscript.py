from expect_helper import *
from test_files import *
from run_helper import *
from test_asserts import *

p = ExpectHelper()
p.start(TEST_FILE1)
p.deposit('12345678', '3333')
p.quit()

assert_test_log()
