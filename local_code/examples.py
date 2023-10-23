import pickle
import socket
import sys
import network_control as nc

def no_params_fun():
    fun={"mod": 0, "idx": 0}
    nc.send_command(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

def fun_with_params(a,b,c):
    fun={"mod": 0, "idx": 1}
    fun["args"] = [a,b,c]
    nc.send_command(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

def varriable_num_of_params(single, *poz, **name):
    fun={"mod": 0, "idx": 2}
    fun["args"] = [single, *poz,]
    fun["kwargs"] = name
    nc.send_command(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

def return_multiple_values(a,b):
    fun={"mod": 0, "idx": 3}
    fun["args"] = [a,b]
    nc.send_command(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

def return_single_value(a):
    fun={"mod": 0, "idx": 4}
    fun["args"] = [a]
    nc.send_command(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

def return_string():
    fun={"mod": 0, "idx": 5}
    nc.send_command(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

def return_none():
    fun={"mod": 0, "idx": 6}
    nc.send_command(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

class WithoutInit:
    def __del__(self):
        fun={"delObjId": id(self)}
        nc.send_command(fun)

    def wait(self, sleep_time):
        fun={"mod": 0, "idx": 7}
        fun["objId"] = id(self)
        fun["args"] = [sleep_time]
        nc.send_command(fun)

        callback = nc.get_function_callback()
        nc.raise_exception_forward(callback)
        return nc.return_value(callback)

    def __init__(self):
        fun={"mod": 0}
        fun["objId"] = id(self)
        fun["init"] = "WithoutInit"
        nc.send_command(fun)

class NoParams:
    def __del__(self):
        fun={"delObjId": id(self)}
        nc.send_command(fun)

    def __init__(self):
        fun={"mod": 0}
        fun["objId"] = id(self)
        fun["init"] = "NoParams"
        nc.send_command(fun)

    def return_five(self):
        fun={"mod": 0, "idx": 8}
        fun["objId"] = id(self)
        nc.send_command(fun)

        callback = nc.get_function_callback()
        nc.raise_exception_forward(callback)
        return nc.return_value(callback)

class Params:
    def __del__(self):
        fun={"delObjId": id(self)}
        nc.send_command(fun)

    def __init__(self, a):
        fun={"mod": 0}
        fun["objId"] = id(self)
        fun["args"] = [a]
        fun["init"] = "Params"
        nc.send_command(fun)

def divide_numbers(a,b):
    fun={"mod": 0, "idx": 9}
    fun["args"] = [a,b]
    nc.send_command(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

class Inherited(NoParams):
    def __del__(self):
        fun={"delObjId": id(self)}
        nc.send_command(fun)

def __init__(self):
    fun={"mod": 0}
    fun["objId"] = id(self)
    fun["init"] = "Inherited"
    nc.send_command(fun)

# import remotely
def _import():
    nc.send_command({"import": 0}) # import module

_import()
