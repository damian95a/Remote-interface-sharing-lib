from examples import *
import pytest

def test_no_exception():
    try:
        divide_numbers(3,7)
    except Exception:
        assert False
    else:
        assert True

def test_zero_division():
    try:
        divide_numbers(10,0)
    except ZeroDivisionError:
        assert True
    except Exception:
        assert False
    else:
        assert False

def test_exception_from_init():
    try:
        obj = NotConstructable()
    except Exception as e:
        assert str(e) == "Exception"
    else:
        assert False