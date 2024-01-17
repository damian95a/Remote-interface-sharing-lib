import module
import pytest

def test_function_call_witt_str_param():
    ret_str = module.fun("abbccc")
    assert ret_str == "Success: abbccc"

def test_function_call_witt_num_param():
    ret_str = module.fun("341")
    assert ret_str == "Success: 341"

def test_module_in_package():
    import package.module.module
    ret_str = package.module.module.fun()
    assert ret_str == "Test"