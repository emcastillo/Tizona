import importlib

def load_module(module_string):
    """
    dynamically load a module from a string
    """
    module = importlib.import_module(module_string)
    return module

def load_class(class_string):
    """
    class_string is the path to the class
    module.class
    """
    tokens = class_string.split(".")
    class_name = tokens[-1]
    module = load_module(".".join(tokens[:-1]))
    return getattr(module, class_str)
