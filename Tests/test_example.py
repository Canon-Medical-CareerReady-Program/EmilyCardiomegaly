import pytest

# This is an example of a test
# Each test file needs to begin with test_*.py
# Each test case function needs to begin with test_ for pytest to discover it
# You can run all tests using a script in Scripts folder or right click here in PyCharm and run with pytest

def test_sample_test():
    assert 1 == 1
    assert 4 == 2*2
    assert "abc"*2 == "abcabc"
    # Uncomment below to see how pytest reports a test failure
    #assert False
