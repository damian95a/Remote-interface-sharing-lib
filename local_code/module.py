import pickle
import socket
import sys
import network_control as nc

def fun(a):
    fun={"mod": 1, "idx": 0, "args": [a]}
    nc.send_function_call(fun)
    
    callback = nc.get_function_callback()
    nc.raise_exception_forward(callback)
    return nc.return_value(callback)


# import remotely
def _import():
    command = pickle.dumps({"import": 1}) # import module
    print(f'Connecting to {nc.server_addr[0]}, port {nc.server_addr[1]}', file=sys.stderr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(nc.server_addr)
    try:
        sock.sendall(command)
    finally:
        sock.close()

_import()