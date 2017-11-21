import os.path
parent = os.path.dirname(os.path.realpath(__file__))
test_dir = os.path.dirname(parent)
file_dir = os.path.join(test_dir, 'etc')

# Records the locations of the input files used by the tests
TEST_FILE1 = os.path.join(file_dir, 'testfile1.txt')
TEST_FILE2 = os.path.join(file_dir, 'testfile2.txt')
