from expect_helper import *
from test_files import *
from run_helper import *
from test_asserts import *

p = ExpectHelper()
p.start(TEST_FILE1)
p.withdraw('12345678', '3333')
p.quit()

assert_test_log()
