def no_params_fun():
    return "Test"

def fun_with_params(a,b,c):
    return f"Test {a}, {b}, {c}"

def varriable_num_of_params(single, *poz, **name):
    str_p  = ' '.join(map(lambda p: str(p), poz))
    str_kw = ' '.join(map(lambda it: f'{it[0]}={it[1]}', name.items()))

    return ' '.join((single, str_p, str_kw))

def return_multiple_values(a,b):
    return a+b, a*b

def return_single_value(a):
    return 2*a

def return_string():
    return "Test - 123"

def return_none():
    return None

def divide_numbers(a,b):
    return a/b

class WithoutInit:
    def wait(self, sleep_time):
        import time
        time.sleep(sleep_time)
        return "ok"

class NoParams:
    def __init__(self):
        print("initialization")
    
    def __del__(self):
        print("deleting")
    
    def return_five(self):
        return 5


class Params:
    def __init__(self, a):
        self.a = a

functions = [no_params_fun,\
            fun_with_params,\
            varriable_num_of_params,\
            return_multiple_values,\
            return_single_value,\
            return_string,\
            return_none,\
            NoParams.return_five,\
            WithoutInit.wait,
            divide_numbers]
