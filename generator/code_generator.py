import os

class CodeGenerator:
    def __init__(self, dir, file, module_id):
        self.direcotry = dir
        self.file = file
        self.module_index = module_id

    def generate_imports(self):
        top = "import pickle\nimport socket\nimport sys\nimport network_control as nc\n"

        with open(f"{self.direcotry}/{self.file}", 'w') as gen_code:
            gen_code.write(top)

    def import_current_module_on_host(self):
        code = ('\n# import remotely\n',\
                'def _import():\n'\
                f'    nc.send_command({{"import": {self.module_index}}}) # import module\n'\
                '\n',\
                '_import()\n'\
                )
        with open(f"{self.direcotry}/{self.file}", 'a') as gen_code:
            gen_code.writelines(code)
    

    def generate_fun_header_data(self, gen_file, code_line, fun_index, tabs, is_class_method):
        name_start = code_line.find('def') + 4
        arg_start = code_line.find('(') + 1
        arg_end = code_line.rfind(')')

        function_name = code_line[name_start:arg_start-1]
        if is_class_method:
            omit_self_pos = code_line[arg_start:].find(',') + 1
            arg_start = arg_start + omit_self_pos if omit_self_pos != 0 else arg_end
        kw_arg = code_line.rfind('**')

        if fun_index is not None:
            gen_file.write(f'{tabs}fun={{"mod": {self.module_index}, "idx": {fun_index}}}\n')
        else:
            gen_file.write(f'{tabs}fun={{"mod": {self.module_index}}}\n')

            
        if is_class_method:
            gen_file.write(f'{tabs}fun["objId"] = id(self)\n')
        if kw_arg == -1 and arg_start != arg_end:
            gen_file.write(f'{tabs}fun["args"] = [{code_line[arg_start:arg_end].strip()}]\n')
        elif arg_start != arg_end:
            gen_file.write(f'{tabs}fun["args"] = [{code_line[arg_start:kw_arg-1]}]\n')
            gen_file.write(f'{tabs}fun["kwargs"] = {code_line[kw_arg+2:arg_end]}\n')

        return function_name
        
    def implement_init_body(self, gen_file, code_line, class_name, tabs):
        self.generate_fun_header_data(gen_file, code_line, None, tabs, True)
        gen_file.write(f'{tabs}fun["init"] = "{class_name}"\n')
        gen_file.write(f'{tabs}nc.send_command(fun)\n')
        
    def implement_default_init(self, class_name, tabs):
        init_def = f'{tabs}def __init__(self):'
        with open(f"{self.direcotry}/{self.file}", 'a') as gen_code:
            gen_code.write('\n'+init_def[4:]+'\n')
            self.implement_init_body(gen_code, init_def, class_name, tabs)


def function_network_implementation(gen_code, tabs):
    gen_code.write(f'{tabs}nc.send_command(fun)\n')
    gen_code.write('\n')
    gen_code.write(f"{tabs}callback = nc.get_function_callback()\n")
    gen_code.write(f"{tabs}nc.raise_exception_forward(callback)\n")