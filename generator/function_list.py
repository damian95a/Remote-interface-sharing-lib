class FunctionListGenerator:
    def __init__(self, dir, module_name, file_name):
        self.directory = dir
        self.functions_list = f"{file_name[:-3]}_func.py"

        with open(f"{self.directory}/{self.functions_list}", 'w') as gen_code: # generating function list
            gen_code.write(f"from {module_name} import *\n\n")
            gen_code.write("functions = [\n")

    def add_function(self, f_name, cl_name):
        with open(f"{self.directory}/{self.functions_list}", 'a') as gen_code: # generating function list
            if not cl_name:
                gen_code.write(f"{' '*12}{f_name},\\\n")
            else:
                gen_code.write(f"{' '*12}{cl_name}.{f_name},\\\n")
    
    def finish(self):
        with open(f"{self.directory}/{self.functions_list}", 'a') as gen_code: # generating function list
            gen_code.write("]\n")