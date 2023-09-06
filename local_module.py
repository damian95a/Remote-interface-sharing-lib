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

def fun(a):
    fun={"mod": 1, "idx": 0, "args": [a]}
    _send_function_call(fun)
    return _get_return_value()


# import remotely
def _import():
    command = pickle.dumps({"import": 1}) # import module
    print(f'Connecting to {server_addr[0]}, port {server_addr[1]}', file=sys.stderr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)
    try:
        sock.sendall(command)
    finally:
        sock.close()

_import()