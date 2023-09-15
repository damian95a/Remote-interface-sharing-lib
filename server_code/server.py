#!/usr/bin/python3
import socket
import sys
import pickle

modules = ("examples",\
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
            exception = None
            returned_value = None
            try:
                if "kwargs" not in command:
                    returned_value = functions[command["idx"]](*args)
                else:
                    returned_value = functions[command["idx"]](*args, **command["kwargs"])
            except Exception as e:
                exception = e

            feedback = {}
            if exception is not None:
                feedback["except"] = exception
            if returned_value is not None:
                feedback["return"] = returned_value

            connection, _ = sock.accept()
            try:
                call_back = pickle.dumps(feedback)
                connection.sendall(call_back)
            finally:
                print("Closing connection", file=sys.stderr)
                connection.close()
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
