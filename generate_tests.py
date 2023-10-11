import sys
import inspect
from gpt_caller import GPTCaller
import traceback

def write_to_file(input_file, output_stream):
    content = open(input_file, "r").read()
    output_stream.write(content)

def fill_function_works(func_name, output_stream):
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

    try:
        return_type = types_dict.get("return").__name__
        content = content.replace("<response_type>", str(return_type))

        response_type_text_dict = {
            "list": "uma lista",
            "bool": "um booleano",
            "int": "um inteiro",
            "float": "um float",
            "str": "uma string",
            "dict": "um dicionário"
        }
        content = content.replace("<response_type_text>", response_type_text_dict.get(return_type))
    except:
        raise Exception("ERROR: Return type not specified for function " + func_name)
    
    try:
        params_call = ""
        parameters_list = parameters_str.split(", ")
        parameters_list = [x.split(":") for x in parameters_list]
        for parameter in parameters_list:
            if parameter[1] == "list" or parameter[1] == "dict":
                params_call += f"deepcopy({parameter[0]}), "
            else:
                params_call += f"{parameter[0]}, "
        params_call = params_call[:-2]
        content = content.replace("<params_call>", params_call)

        parameter_input = ""
        for parameter in parameters_list:
            if parameter[1] == "list" or parameter[1] == "dict":
                parameter_input += f'{parameter[0]}: \\n{ {parameter[0]} }, '
            else:
                parameter_input += f'{parameter[0]}: { {parameter[0]} }, '
        parameter_input = parameter_input.replace("'", "")
        parameter_input = parameter_input[:-2]
        content = content.replace("<parameter_input>", parameter_input)
    except:
        raise Exception("ERROR: Could not generate params call for function " + func_name + ". Check if the parameters are correctly typed.")

    output_stream.write(content)

def fill_test(func_name, output_stream, tests):
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
        docstring = docstring.split("\n")
        level = docstring[0]
        content = content.replace("<level>", level)
    
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
        functions = [x for x in dir(module) if not x.startswith('__') and callable(getattr(module, x))]
    except:
        print("ERROR: Invalid input file. Could not correctly import module.")
        sys.exit(1)

    f = open("test_.py", "w")
    write_to_file("snippets/imports.py", f)
    
    for function in functions:
        f.write(f'''try:
    if funcoes:
        from funcoes import {function}
except:
    pass        
''')
    f.write("\nPWD = Path(__file__).parent\n")
    f.write("program = PWD / 'programa.py'\n")
    
    write_to_file("snippets/funcoes_proibidas.py", f)

    if gptfill:
        gpt = GPTCaller()
        print("Generating tests with GPT-3. This may take a while...")

        for function in functions:
            fill_function_works(function, f)

            print("Generating tests for function " + function + "...")
            code = inspect.getsource(getattr(module, function))
            tests = gpt.get_tests(gpt_amount, code)
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
                params = (", ".join([ f"test[{i}]" for i in range(len(test)) ]))
                try:
                    exec(f"obtido = module.{function}({params})")
                    test_list_final.append(test + (obtido,))
                except Exception as e:
                    print(f"WARNING: Could not execute tests for function {function}. {type(e).__name__} {e}")
                    traceback.print_exception(*sys.exc_info())
                    success = False
                    test_list_final.append(test)
            join_string = ",\n\t\t\t"
            if not success:
                join_string += "#"
            test_final = join_string.join([ str(x) for x in test_list_final])
            if not success:
                test_final = "#" + test_final
            fill_test(function, f, f"[\n\t\t\t{test_final}\n\t\t]")
    else:
        for function in functions:
            fill_function_works(function, f)
            fill_test(function, f, "[]")

    print("Tests generated successfully!")