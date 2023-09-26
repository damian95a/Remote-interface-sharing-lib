from examples import *
import pytest

def test_return_multiple_values():
    a,b = return_multiple_values(3,4)
    assert a == 7
    assert b == 12

def test_return_single_value():
    a = return_single_value(7)
    assert a == 14

def test_return_string():
    s = return_string()
    assert s == "Test - 123"

def test_return_none():
    a = return_none()
    assert a is None

def test_divide_numbers():
    a = divide_numbers(5,2)
    delta = 1e-4
    assert 2.5-delta < a and a < 2.5+delta