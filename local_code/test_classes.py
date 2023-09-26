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