from examples import *
import pytest

def test_no_params():
    s = no_params_fun()
    assert s == "Test"

def test_regular_params():
    s = fun_with_params(1, "asd", [1,])
    assert s == "Test 1, asd, [1]"

def test_variable_num_of_params():
    s = varriable_num_of_params("PyTest:", 1, 12, 'cba', a='xyz', b=-5)
    assert s == "PyTest: 1 12 cba a=xyz b=-5"