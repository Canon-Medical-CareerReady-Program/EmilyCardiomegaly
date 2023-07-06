import pytest
from Cardiomegaly.point import Point

# This is an example of a test
# Each test file needs to begin with test_*.py
# Each test case function needs to begin with test_ for pytest to discover it
# You can run all tests using a script in Scripts folder or right click here in PyCharm and run with pytest

def test_sample_test():
    a = Point(567.89, 12.78)
    assert a.x == 567.89
    assert a.y == 12.78
    a.x = 0 
    a.y = 0
    assert a.x ==0
    assert a.y ==0
    # Uncomment below to see how pytest reports a test failure
    #assert False
