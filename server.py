#!/usr/bin/python3
import socket
import sys
import pickle

modules = ("onserver_code",\
           "module")

def inModules(idx):
    return idx >= 0 and idx < len(modules)

NonePickledObj = pickle.dumps(None)
objects = {}

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_addr = ('localhost', 10_000)
    print(f'starting up on {server_addr[0]}, port {server_addr[1]}', file=sys.stderr)
    sock.bind(server_addr)

    sock.listen(2)


    while True:
        print("Waiting for a command", file=sys.stderr)
        command = b''
        connection, _ = sock.accept()

        try:
            while data := connection.recv(8):
                command += data
        finally:
            print("Closing connection", file=sys.stderr)
            connection.close()

        command = pickle.loads(command)
        args = command["args"] if "args" in command else []
        if "idx" in command and "mod" in command:
            if not inModules(command["mod"]):
                print("WRONG MODULE NAME!")
                continue

            if "objId" in command:
                args.insert(0, objects[command["objId"]])
            functions = eval(f'{modules[command["mod"]]}.functions')
                
            if "kwargs" not in command:
                returned_value = functions[command["idx"]](*args)
            else:
                returned_value = functions[command["idx"]](*args, **command["kwargs"])

            if returned_value is not None:
                connection, _ = sock.accept()
                try:
                    call_back = pickle.dumps(returned_value)
                    connection.sendall(call_back)
                finally:
                    print("Closing connection", file=sys.stderr)
                    connection.close()
            else:
                sock.settimeout(0.05)
                try:
                    connection, _ = sock.accept()
                except socket.timeout: # TimeoutError: # dla pythona 3.10
                    pass
                else:
                    try:
                        connection.sendall(NonePickledObj)
                    finally:
                        print("Closing connection", file=sys.stderr)
                        connection.close()
                finally:
                    sock.settimeout(None)
        elif "init" in command and "objId" in command and "mod" in command:
            if not inModules(command["mod"]):
                print("WRONG MODULE NAME!")
                continue
            module = modules[command["mod"]]
            if "kwargs" not in command:
                objects[command["objId"]] = eval(''.join((module, '.', command["init"], '(*args)')))
            else:
                objects[command["objId"]] = eval(''.join((module, '.', command["init"], '(*args, **command["kwargs"])')))
        elif "delObjId" in command:
            if command["delObjId"] in objects:
                del objects[command["delObjId"]]
        elif "import" in command:
            if not inModules(command["import"]):
                print("WRONG MODULE NAME!")
                continue
            exec(f"import {modules[command['import']]}")

finally:
    print("Closing socket")
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
