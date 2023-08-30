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

def _get_return_value(buff_size=10):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)
    try:
        return_value = b''
        while call_back := sock.recv(10):
            return_value += call_back
    finally:
        sock.close()
    
    return pickle.loads(return_value)

def no_params_fun():
    fun={"idx": 0}
    _send_function_call(fun)
    
def fun_with_params(a,b,c):
    fun={"idx": 1}
    fun["args"] = [a,b,c]
    _send_function_call(fun)

def varriable_num_of_params(single, *poz,**name):
    fun={"idx": 2}
    fun["args"] = [single, *poz]
    fun["kwargs"] = name
    _send_function_call(fun)
    
def return_multiple_values(a,b):
    fun={"idx": 3}
    fun["args"] = [a,b]
    _send_function_call(fun)
    return _get_return_value()

def return_single_value(a):
    fun={"idx": 4}
    fun["args"] = [a,]
    _send_function_call(fun)
    return _get_return_value()

def return_string():
    fun={"idx": 5}
    _send_function_call(fun)
    return _get_return_value()

def return_none():
    fun={"idx": 6}
    _send_function_call(fun)
    return _get_return_value()

#########

class WithoutInit:
    def __init__(self):
        meth = {"init": "onserver_code.WithoutInit", "objId": id(self)}
        _send_function_call(meth)
    
    def __del__(self):
        meth = {"delObjId": id(self)}
        _send_function_call(meth)

    def wait(self, sleep_time):
        meth={"idx": 8, "objId": id(self), "args": [sleep_time]}
        _send_function_call(meth)
        return _get_return_value()

class NoParams:
    def __init__(self):
        meth = {"init": "onserver_code.NoParams", "objId": id(self)}
        _send_function_call(meth)
    
    def __del__(self):
        meth = {"delObjId": id(self)}
        _send_function_call(meth)

    def return_five(self):
        meth={"idx": 7, "objId": id(self)}
        _send_function_call(meth)
        return _get_return_value()


class Params:
    def __init__(self, a):
        meth = {"init": "onserver_code.Params", "objId": id(self)}
        meth["args"] = [a]
        _send_function_call(meth)

    def __del__(self):
        meth = {"delObjId": id(self)}
        _send_function_call(meth)