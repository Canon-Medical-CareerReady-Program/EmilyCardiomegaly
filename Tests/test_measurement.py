import pytest
from Cardiomegaly.measurement import Measurement


# This is an example of a test
# Each test file needs to begin with test_*.py
# Each test case function needs to begin with test_ for pytest to discover it
# You can run all tests using a script in Scripts folder or right click here in PyCharm and run with pytest

def test_body_part():
    a = Measurement("Heart")
    assert a.body_part == "Heart"
    a.body_part = "Thorax"
    assert a.body_part =="Thorax"

def test_length(): 
    pinnochio = Measurement("nose")
    pinnochio.end.x = 100
    assert pinnochio.end.x == 100
    assert pinnochio.length() == 100


    # Uncomment below to see how pytest reports a test failure
    #assert False
