import sys
import inspect
from gpt_caller import GPTCaller
from utils import *
import os

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("ERROR: Invalid number of arguments")
        print("USAGE: python generate_statements.py <input_file> <test_name>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    test_name = sys.argv[2]
    try:
        module_name = sys.argv[1].replace('.py', '')
        module = __import__(module_name)
        functions = get_function_names_in_order_of_appearence(module)
        function_levels = get_function_levels(module, functions)
    except Exception as e:
        print(f"ERROR: Could not correctly import module. Please copy the input file to the same directory as this script. \n{e}")
        sys.exit(1)

    if not os.path.exists(test_name):
        os.mkdir(test_name)

    levels = set ([ val for val in function_levels.values() ])
    phases = {}
    for level in levels:
        phases[level] = 1
        f = open(f"{test_name}/{level}.md", "w")
        f.write(f"# {level.capitalize()}\n\n")
        f.close()

    gpt = GPTCaller()
    print(f"Generating statements with {gpt.model}. This may take a while...")

    for function in functions:
        print("Generating statement for function " + function + "...")
        level = function_levels[function]
        code = inspect.getsource(getattr(module, function))
        statement = gpt.get_statement(code)
        file = open(f"{test_name}/{level}.md", "a")
        file.write(f"## Etapa {phases[level]}\n\n")
        phases[level] += 1
        file.write(statement)
        file.write("\n\n___\n\n")
        file.close()
    
    print("Statements generated. Check the output folder.")