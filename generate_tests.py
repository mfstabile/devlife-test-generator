import sys
import inspect
from gpt_caller import GPTCaller
import traceback
import random
from copy import deepcopy
from utils import *

def fill_function_works(func_name, output_stream, random_seed=-1):
    content = open("snippets/funcao_funciona.py", "r").read()
    content = content.replace("<func_name>", func_name)
    function = (getattr(module, func_name))
    parameters = (inspect.signature(getattr(module, func_name)))
    parameter_num = len(parameters.parameters)

    parameters_str = str(parameters).replace("(", "").replace(")", "").replace(" ", "").split(",")
    parameters_str = [x for x in parameters_str if x != ""]
    parameters_str = ", ".join(parameters_str)
    parameters_str = parameters_str.split("->")[0]
    content = content.replace("<parameters>", parameters_str)

    content = content.replace("<expected_params>", str(parameter_num))

    types_dict = function.__annotations__

    if random_seed != -1:
        content = content.replace("<random_text>", f"\n    random.seed({random_seed})")
    else:
        content = content.replace("<random_text>", "")

    try:
        return_type = types_dict.get("return").__name__
        content = content.replace("<response_type>", str(return_type))
        if return_type == "str":
            content = content.replace("<expected_text>", '"{esperado}"')
        else:
            content = content.replace("<expected_text>", "{esperado}")

        response_type_text_dict = {
            "list": "uma lista",
            "bool": "um booleano",
            "int": "um inteiro",
            "float": "um float",
            "str": "uma string",
            "dict": "um dicionário"
        }
        content = content.replace("<response_type_text>", response_type_text_dict[return_type])
    except:
        raise Exception("ERROR: Return type not specified for function " + func_name)
    
    try:
        params_call = ""
        if parameters_str != "":
            parameters_list = parameters_str.split(", ")
            parameters_list = [x.split(":") for x in parameters_list]
            for parameter in parameters_list:
                if parameter[1] == "list" or parameter[1] == "dict":
                    params_call += f"deepcopy({parameter[0]}), "
                else:
                    params_call += f"{parameter[0]}, "
            params_call = params_call[:-2]
        else:
            print("WARNING: Function " + func_name + " has no parameters. This may lead to unexpected behavior.")
            params_call = ""
            parameters_list = []
        content = content.replace("<params_call>", params_call)

        parameter_input = ""
        for parameter in parameters_list:
            if parameter[1] == "list" or parameter[1] == "dict":
                parameter_input += f'{parameter[0]}: \\n{ {parameter[0]} }, '
            else:
                parameter_input += f'{parameter[0]}: { {parameter[0]} }, '
        if parameter_input != "":
            parameter_input = parameter_input.replace("'", "")
            parameter_input = parameter_input[:-2]
        content = content.replace("<parameter_input>", parameter_input)
    except:
        raise Exception("ERROR: Could not generate params call for function " + func_name + ". Check if the parameters are correctly typed.")

    output_stream.write(content)

def fill_test(func_name, phase, output_stream, tests):
    content = open("snippets/test.py", "r").read()
    content = content.replace("<func_name>", func_name)

    parameters = (inspect.signature(getattr(module, func_name)))
    parameter_num = len(parameters.parameters)

    parameters_str = str(parameters).replace("(", "").replace(")", "").replace(" ", "").split(",")
    parameters_str = [x.split(":")[0] for x in parameters_str if x != ""]
    parameters_str = ", ".join(parameters_str)
    parameters_str = parameters_str.split("->")[0]
    content = content.replace("<parameters>", parameters_str)

    parameters_list = parameters_str.split(", ")

    parameter_input = ""
    for parameter in parameters_list:
        parameter_input += f'{parameter}: { {parameter} }, '
    parameter_input = parameter_input.replace("'", "")
    parameter_input = parameter_input[:-2]
    content = content.replace("<parameter_input>", parameter_input)

    #get docstring
    function = (getattr(module, func_name))
    docstring = function.__doc__
    if docstring is None:
        print("WARNING: Docstring not found for function " + func_name)
    else:
        docstring = docstring.strip().split("\n")
        level = docstring[0]
        content = content.replace("<level>", level)
    
    content = content.replace("<phase>", f"{phase}")

    content = content.replace("<tests>", tests)

    output_stream.write(content)

if __name__ == "__main__":

    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("ERROR: Invalid number of arguments")
        print("USAGE: python generate_tests.py <input_file> -gpt(optional) <test_amount>(default 5)>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    gptfill = len(sys.argv) >= 3 and sys.argv[2] == "-gpt"
    gpt_amount = 5
    if gptfill and len(sys.argv) == 4:
        gpt_amount = int(sys.argv[3])

    try:
        module_name = sys.argv[1].replace('.py', '')
        module = __import__(module_name)
        functions = get_function_names_in_order_of_appearence(module)
        function_levels = get_function_levels(module, functions)
    except Exception as e:
        print(f"ERROR: Could not correctly import module. Please copy the input file to the same directory as this script. \n{e}")
        sys.exit(1)

    f = open("test_.py", "w")
    write_to_file("snippets/imports.py", f)
    
    levels = set ([ val for val in function_levels.values() ])
    phases = {}
    for level in levels:
        phases[level] = 1

    random_calls = []
    for function in functions:
        if check_random_calls_in_function(getattr(module, function)):
            random_calls.append(function)
        f.write(f'''try:
    if funcoes:
        from funcoes import {function}
except:
    pass
''')
    f.write("\nPWD = Path(__file__).parent\n")
    f.write("program = PWD / 'programa.py'\n")
    write_to_file("snippets/funcoes_auxiliares.py", f)

    if gptfill:
        gpt = GPTCaller()
        print(f"Generating tests with {gpt.model}. This may take a while...")
        random_seed = random.randint(11,99)

        for function in functions:
            fill_function_works(function, f, random_seed if function in random_calls else -1)

            print("Generating tests for function " + function + "...")
            code = inspect.getsource(getattr(module, function))
            tests = gpt.get_tests(gpt_amount, code)
            print("Tests generated for function " + function + ":")
            print(tests)
            print("#" * 50)
            tests_ = []
            try:
                exec("tests_ = " + tests)
            except:
                print("ERROR: Could not generate tests for function " + function + ". Trying to recover...")
                test_list = tests.split(",")
                i = -1
                while len(test_list[:i]) > 0:
                    try:
                        fix = ",".join(test_list[:i]) + "]"
                        exec("tests_ = " + fix)
                        print(f"Recovered! {function} tests generated. Some tests may be missing.")
                        break
                    except:
                        pass
                    i -= 1
                if len(test_list[:i]) == 0:
                    print("ERROR: Could not recover tests for function " + function + ".")
            test_list_final = []
            success = True
            for test in tests_:
                params = (", ".join([ f"deepcopy(test[{i}])" for i in range(len(test)) ]))

                try:
                    random.seed(random_seed)
                    exec(f"obtido = module.{function}({params})")
                    test_list_final.append(test + (obtido,))
                except Exception as e:
                    print(f"WARNING: Could not execute tests for function {function}.")
                    # traceback.print_exception(*sys.exc_info())
                    success = False
                    test_list_final.append(test)
            join_string = ",\n\t\t\t"
            if not success:
                join_string += "#"
            test_final = join_string.join([ str(x) for x in test_list_final])
            if not success:
                test_final = "#" + test_final
            level = function_levels[function]
            fill_test(function, phases[level], f, f"[\n\t\t\t{test_final},\n\t\t]")
            phases[level] += 1
    else:
        for function in functions:
            fill_function_works(function, f)
            level = function_levels[function]
            fill_test(function, phases[level], f, "[]")
            phases[level] += 1

    print("Tests generation has finished!")