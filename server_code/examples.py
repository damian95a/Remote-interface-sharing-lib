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

def no_return():
    pass

def default_param(a=7, b=5):
    return a,b

class WithoutInit:
    def wait(self, sleep_time):
        import time
        time.sleep(sleep_time)
        return "ok"

class NoParams:
    def __init__(self):
        print("initialization")
        self.__text = "Private"

    def __del__(self):
        print("deleting")
    
    def return_five(self):
        return 5

    def __get_str(self):
        return self.__text


class Params:
    def __init__(self, a):
        self.a = a

def divide_numbers(a,b):
    return a/b

class Inherited(NoParams):
    pass

class NotConstructable:
    def __init__(self):
        raise Exception("Exception")

class Printable:
    def __str__(self):
        return "<class Printable object>"

class Cloneable:
    def __init__(self, a):
        self.a = a

    def get(self):
        return self.a

    def clone(self):
        return Cloneable(self.a)

def get_value(obj):
    return obj.get()

class Structure:
    def __init__(self):
        self.a = 3
    
    def get_a(self):
        return self.a

    def set_a(self, a):
        self.a = a