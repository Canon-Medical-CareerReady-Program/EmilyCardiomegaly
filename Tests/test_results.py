import pytest
from Cardiomegaly.results import Result


# This is an example of a test
# Each test file needs to begin with test_*.py
# Each test case function needs to begin with test_ for pytest to discover it
# You can run all tests using a script in Scripts folder or right click here in PyCharm and run with pytest

def test_variables():
    a = Result("00000_1")
    assert a.image_name == "00000_1"
    assert a.heart.body_part == "Heart"
    assert a.thorax.body_part == "Thorax"


    # Uncomment below to see how pytest reports a test failure
    #assert False
