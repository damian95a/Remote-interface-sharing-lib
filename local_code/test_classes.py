from examples import *
import pytest
import network_control as nc
from time import time

# WithoutInit
def test_WithoutInit_wait_mathod():
    n = nc.get_num_of_objects()
    assert n == 0

    o = WithoutInit()
    n = nc.get_num_of_objects()
    assert n == 1

    start = time()
    expect = 1.2
    o.wait(expect)
    duration = time() - start
    assert abs(duration - expect) < 0.5

    del o
    n = nc.get_num_of_objects()
    assert n == 0

def test_multiple_instances_of_WithoutInit():
    n = nc.get_num_of_objects()
    assert n == 0

    o1 = WithoutInit()
    o2 = WithoutInit()
    n = nc.get_num_of_objects()
    assert n == 2

    del o1
    n = nc.get_num_of_objects()
    assert n == 1

def test_override_instance_of_WithoutInit():
    n = nc.get_num_of_objects()
    assert n == 0

    o = WithoutInit()
    n = nc.get_num_of_objects()
    assert n == 1

    o = WithoutInit()
    n = nc.get_num_of_objects()
    assert n == 1

    del o
    n = nc.get_num_of_objects()
    assert n == 0

def test_class_method():
    obj = NoParams()

    value = obj.return_five()
    assert value == 5

def test_deriverred_method():
    obj = Inherited()
    
    value = obj.return_five()
    assert value == 5

def test_instances_no_for_derrivered_class():
    obj = Inherited()

    n = nc.get_num_of_objects()
    assert n == 1

def test_wrond_object():
    not_local = Cloneable(5).clone()
    
    try:
        not_local.get()
    except ValueError:
        assert True
    else:
        assert False

def test_string_conversion():
    obj = Printable()

    assert str(obj) == "<class Printable object>"

def test_getter():
    obj = Structure()

    assert obj.get_a() == 3

def test_getter_setter():
    obj = Structure()
    obj.set_a(7)

    assert obj.get_a() == 7