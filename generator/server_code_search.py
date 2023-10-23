import string

def find_function_def(code_line):
    pos = code_line.find('def')

    if pos != -1:
        start_name = pos + 4
        end_name = code_line.find('(')

        return pos, code_line[start_name:end_name]
    return pos, None

def find_class_def(code_line):
    pos = code_line.find('class')

    if pos != -1:
        class_name = code_line.split()[1]
        name_end = class_name.find('(')
        if name_end == -1:
            name_end = class_name.find(':')
        class_name = class_name[:name_end]

        return pos, class_name
    return pos, None

def end_of_class(code_line, class_indent):
    return any(l not in string.whitespace for l in code_line[0:class_indent])
