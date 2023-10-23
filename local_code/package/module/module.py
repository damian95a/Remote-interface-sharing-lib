import pickle
import socket
import sys
import network_control as nc

def fun():
    fun={"mod": 2, "idx": 0}
    nc.send_command(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

# import remotely
def _import():
    nc.send_command({"import": 2}) # import module

_import()
