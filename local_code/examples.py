import pickle
import socket
import sys
import network_control as nc

def no_params_fun():
    fun={"mod": 0, "idx": 0}
    nc.send_function_call(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    
def fun_with_params(a,b,c):
    fun={"mod": 0, "idx": 1}
    fun["args"] = [a,b,c]
    nc.send_function_call(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)

def varriable_num_of_params(single, *poz,**name):
    fun={"mod": 0, "idx": 2}
    fun["args"] = [single, *poz]
    fun["kwargs"] = name
    nc.send_function_call(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    
def return_multiple_values(a,b):
    fun={"mod": 0, "idx": 3}
    fun["args"] = [a,b]
    nc.send_function_call(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

def return_single_value(a):
    fun={"mod": 0, "idx": 4}
    fun["args"] = [a,]
    nc.send_function_call(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

def return_string():
    fun={"mod": 0, "idx": 5}
    nc.send_function_call(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

def return_none():
    fun={"mod": 0, "idx": 6}
    nc.send_function_call(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

def divide_numbers(a,b):
    fun={"mod": 0, "idx": 9}
    fun["args"] = [a,b]
    nc.send_function_call(fun)

    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)

#########

class WithoutInit:
    def __init__(self):
        print("Wchodzi w init")
        meth = {"mod": 0, "init": "WithoutInit", "objId": id(self)}
        nc.send_function_call(meth)
    
    def __del__(self):
        meth = {"delObjId": id(self)}
        nc.send_function_call(meth)

    def wait(self, sleep_time):
        meth={"mod": 0, "idx": 8, "objId": id(self), "args": [sleep_time]}
        nc.send_function_call(meth)

        callback = nc.get_function_callback()
        nc.raise_exception_forward(callback)
        return nc.return_value(callback)

class NoParams:
    def __init__(self):
        meth = {"mod": 0, "init": "NoParams", "objId": id(self)}
        nc.send_function_call(meth)
    
    def __del__(self):
        meth = {"delObjId": id(self)}
        nc.send_function_call(meth)

    def return_five(self):
        meth={"mod": 0, "idx": 7, "objId": id(self)}
        nc.send_function_call(meth)

        callback = nc.get_function_callback()
        nc.raise_exception_forward(callback)
        return nc.return_value(callback)


class Params:
    def __init__(self, a):
        meth = {"mod": 0, "init": "Params", "objId": id(self)}
        meth["args"] = [a]
        nc.send_function_call(meth)

    def __del__(self):
        meth = {"delObjId": id(self)}
        nc.send_function_call(meth)

# import remotely
def _import():
    command = pickle.dumps({"import": 0}) # import onserver_code
    print(f'Connecting to {nc.server_addr[0]}, port {nc.server_addr[1]}', file=sys.stderr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(nc.server_addr)
    try:
        sock.sendall(command)
    finally:
        sock.close()

_import()