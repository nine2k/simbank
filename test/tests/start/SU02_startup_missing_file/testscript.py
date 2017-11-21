from expect_helper import *
from test_files import *
from run_helper import *
from test_asserts import *

p = ExpectHelper()
p.start()
p.expect_error()

assert_test_log()
