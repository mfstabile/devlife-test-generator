import inspect
import ast
from random_call_visitor import RandomCallVisitor

def write_to_file(input_file, output_stream):
    content = open(input_file, "r").read()
    output_stream.write(content)

def check_random_calls_in_function(func):
    source = inspect.getsource(func)
    tree = ast.parse(source)
    visitor = RandomCallVisitor()
    visitor.visit(tree)
    return visitor.found_random_call

def get_function_names_in_order_of_appearence(module_name):

    this_source = inspect.getsource(module_name)
    tree = ast.parse(this_source)
    functions = []
    
    for elem in tree.body:
        if type(elem) is ast.FunctionDef:
            this_func_name = elem.name
            functions.append(this_func_name)
            
    return functions

def get_function_levels(module, functions):
    level_dict = {}
    for func_name in functions:
        #get docstring
        function = (getattr(module, func_name))
        docstring = function.__doc__
        if docstring is None:
            print("WARNING: Docstring not found for function " + func_name)
            level = "outro"
        else:
            docstring = docstring.strip().split("\n")
            level = docstring[0]
        level_dict[func_name] = level
    return level_dict    
    