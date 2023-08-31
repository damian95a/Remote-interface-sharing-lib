import pickle
import socket
import sys

server_addr = ('localhost', 10_000)

def _send_function_call(fun_description):
    command = pickle.dumps(fun_description)
    print(f'Connecting to {server_addr[0]}, port {server_addr[1]}', file=sys.stderr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)
    try:
        sock.sendall(command)
    finally:
        sock.close()

def _get_function_callback(buff_size=10):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)
    try:
        callback = b''
        while cb := sock.recv(buff_size):
            callback += cb
    finally:
        sock.close()
    
    return pickle.loads(callback)

def _return_value(callback):
    if "return" in callback:
        return callback["return"]

def _raise_exception_forward(callback):
    if "except" in callback:
        raise callback["except"]

####

def no_params_fun():
    fun={"mod": 0, "idx": 0}
    _send_function_call(fun)

    callback = _get_function_callback()
    _raise_exception_forward(callback)
    
def fun_with_params(a,b,c):
    fun={"mod": 0, "idx": 1}
    fun["args"] = [a,b,c]
    _send_function_call(fun)

    callback = _get_function_callback()
    _raise_exception_forward(callback)

def varriable_num_of_params(single, *poz,**name):
    fun={"mod": 0, "idx": 2}
    fun["args"] = [single, *poz]
    fun["kwargs"] = name
    _send_function_call(fun)

    callback = _get_function_callback()
    _raise_exception_forward(callback)
    
def return_multiple_values(a,b):
    fun={"mod": 0, "idx": 3}
    fun["args"] = [a,b]
    _send_function_call(fun)

    callback = _get_function_callback()
    _raise_exception_forward(callback)
    return _return_value(callback)

def return_single_value(a):
    fun={"mod": 0, "idx": 4}
    fun["args"] = [a,]
    _send_function_call(fun)

    callback = _get_function_callback()
    _raise_exception_forward(callback)
    return _return_value(callback)

def return_string():
    fun={"mod": 0, "idx": 5}
    _send_function_call(fun)

    callback = _get_function_callback()
    _raise_exception_forward(callback)
    return _return_value(callback)

def return_none():
    fun={"mod": 0, "idx": 6}
    _send_function_call(fun)

    callback = _get_function_callback()
    _raise_exception_forward(callback)
    return _return_value(callback)

def divide_numbers(a,b):
    fun={"mod": 0, "idx": 9}
    fun["args"] = [a,b]
    _send_function_call(fun)

    callback = _get_function_callback()
    _raise_exception_forward(callback)
    return _return_value(callback)

#########

class WithoutInit:
    def __init__(self):
        print("Wchodzi w init")
        meth = {"mod": 0, "init": "WithoutInit", "objId": id(self)}
        _send_function_call(meth)
    
    def __del__(self):
        meth = {"delObjId": id(self)}
        _send_function_call(meth)

    def wait(self, sleep_time):
        meth={"mod": 0, "idx": 8, "objId": id(self), "args": [sleep_time]}
        _send_function_call(meth)

        callback = _get_function_callback()
        _raise_exception_forward(callback)
        return _return_value(callback)

class NoParams:
    def __init__(self):
        meth = {"mod": 0, "init": "NoParams", "objId": id(self)}
        _send_function_call(meth)
    
    def __del__(self):
        meth = {"delObjId": id(self)}
        _send_function_call(meth)

    def return_five(self):
        meth={"mod": 0, "idx": 7, "objId": id(self)}
        _send_function_call(meth)

        callback = _get_function_callback()
        _raise_exception_forward(callback)
        return _return_value(callback)


class Params:
    def __init__(self, a):
        meth = {"mod": 0, "init": "Params", "objId": id(self)}
        meth["args"] = [a]
        _send_function_call(meth)

    def __del__(self):
        meth = {"delObjId": id(self)}
        _send_function_call(meth)

# import remotely
def _import():
    command = pickle.dumps({"import": 0}) # import onserver_code
    print(f'Connecting to {server_addr[0]}, port {server_addr[1]}', file=sys.stderr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)
    try:
        sock.sendall(command)
    finally:
        sock.close()

_import()