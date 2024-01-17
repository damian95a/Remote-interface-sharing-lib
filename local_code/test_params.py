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

def test_remote_class_as_parameter():
    obj = Cloneable(3)
    
    cpy = obj.clone()
    value = get_value(cpy)
    value = get_value(obj.clone())
    assert value == 3

def test_fun_with_default_param():
    a,b = default_param()

    assert a == 7
    assert b == 5

def test_override_default_param():
    arg = (4,3)
    values = default_param(*arg)

    assert values == arg