from expect_helper import *
from test_files import *
from run_helper import *
from test_asserts import *

p = ExpectHelper()
p.start(TEST_FILE2+" "+TEST_FILE1)
p.expect_error()

assert_test_log()
