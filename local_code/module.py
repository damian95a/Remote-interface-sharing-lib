import pickle
import socket
import sys
import network_control as nc

def fun(a):
    fun={"mod": 1, "idx": 0, "args": [a]}
    nc.send_command(fun)
    
    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)


# import remotely
def _import():
    nc.send_command({"import": 1}) # import module

_import()