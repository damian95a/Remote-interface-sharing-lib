#!/usr/bin/python3

import os
import sys
from enum import Enum
from function_list import FunctionListGenerator
from server_code_search import *
from code_generator import *
from glob import glob

class FunctionType(Enum):
    RegularFunctionOrMethod = 1
    InitMethod = 2
    DelOperator = 3
    NoneFunction = 0

if len(sys.argv) < 2:
    sys.exit()

dir = "generated_files"
search_dir = sys.argv[1] if sys.argv[1][-1] != '/' else sys.argv[1][:-1]
module_name_start = len(search_dir)+1
exclude_list = ('modules_list.py', 'server.py')

files = tuple(file[module_name_start:] for file in glob(f"{search_dir}/**/*.py", recursive=True) if file[-8:] != "_func.py" and file[module_name_start:] not in exclude_list)
modules = tuple(file[:-3].replace('/', '.') for file in files)

module_index = 0
for file, module_name in zip(files, modules):
    fun_index = 0
    function_type = FunctionType.NoneFunction

    if (slash_pos := file.rfind('/')) != -1:
        os.makedirs(f"{dir}/{file[:slash_pos]}", exist_ok=True)

    try:
        os.mkdir(dir)
    except FileExistsError:
        pass

    function_list = FunctionListGenerator(dir, module_name, file)
    gen = CodeGenerator(dir, file, module_index)

    with open(f"{search_dir}/{file}", 'r') as server_code:
        gen.generate_imports()

        fun_indent = 0
        class_name = ''
        class_indent = 0
        init_implemented = False
        while l := server_code.readline():
            cp, clname = find_class_def(l)

            if end_of_class(l, class_indent):
                if not init_implemented:
                    gen.implement_default_init(class_name, tabs)

                class_name = ''
                class_indent = 0

            if clname is not None:
                class_name = clname
                class_indent = cp+4
                
                init_implemented = False
                with open(f"{dir}/{file}", 'a') as gen_code:
                    gen_code.writelines(('\n', l))

                    gen_code.write(f'{" "*class_indent}def __del__(self):\n')
                    gen_code.write(f'{" "*(class_indent+4)}fun={{"delObjId": id(self)}}\n')
                    gen_code.write(f'{" "*(class_indent+4)}nc.send_command(fun)\n')
                

            if fun_indent>0 and all(x in string.whitespace for x in l[0:fun_indent]):
                if l[fun_indent:].find('return') != -1:
                    with open(f"{dir}/{file}", 'a') as gen_code:
                        gen_code.write(f"{tabs}return nc.return_value(callback)\n")
            else:
                fun_indent = 0


            p, fname = find_function_def(l)
            if fname is not None:
                if class_name:
                    print(f'{class_name}.{fname}')
                else:
                    print(fname)

            if p != -1:
                if l.find('__init__(') != -1:
                    function_type = FunctionType.InitMethod
                elif l.find('__del__(') != -1:
                    function_type = FunctionType.DelOperator
                    continue
                elif l[p+3:].find('__') != -1:
                    function_type = NoneFunction
                    continue
                else:
                    function_type = FunctionType.RegularFunctionOrMethod

                tabs = ' '*(p+4) # czy taby to spacje?
                fun_indent = len(tabs)
                
                with open(f"{dir}/{file}", 'a') as gen_code:
                    gen_code.writelines(('\n', l))
                    # może zastosować match-case ???
                    if function_type == FunctionType.RegularFunctionOrMethod:
                        function_name = gen.generate_fun_header_data(\
                            gen_code, l, fun_index, tabs, class_indent>0)
                        function_network_implementation(gen_code, tabs)
                        function_list.add_function(function_name, class_name)
                        fun_index += 1
                    elif function_type == FunctionType.InitMethod:
                        gen.implement_init_body(gen_code, l, class_name, tabs)
                        init_implemented = True
                    elif function_type == FunctionType.DelOperator:
                        pass
                    else:
                        raise Exception("This code shouldn't have been executed - not recognized function.")

    function_list.finish()
    gen.import_current_module_on_host()
    module_index += 1

with open(f"{dir}/modules_list.py", 'w') as modules_file:
    modules_file.write(f"modules = {modules}")
