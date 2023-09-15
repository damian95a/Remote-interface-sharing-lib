import pickle
import socket
import sys

server_addr = ('localhost', 10_000)

def send_function_call(fun_description):
    command = pickle.dumps(fun_description)
    print(f'Connecting to {server_addr[0]}, port {server_addr[1]}', file=sys.stderr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)
    try:
        sock.sendall(command)
    finally:
        sock.close()

def get_function_callback(buff_size=10):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)
    try:
        callback = b''
        while cb := sock.recv(buff_size):
            callback += cb
    finally:
        sock.close()
    
    return pickle.loads(callback)

def return_value(callback):
    if "return" in callback:
        return callback["return"]

def raise_exception_forward(callback):
    if "except" in callback:
        raise callback["except"]
