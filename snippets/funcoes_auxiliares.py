
def assert_nao_usa_funcoes_proibidas():
    assert funcoes is not None, 'Não foi possível importar o módulo funcoes. Verifique se o código não contém nenhum erro de sintaxe ou uso de input.'
    source = getsource(funcoes)
    
    ex_ast = ast.parse(source)
    funcoes_proibidas = ['min', 'max', 'sum', 'filter', 'map']
    for node in ast.walk(ex_ast):
        if isinstance(node, ast.Call):
            for func_name in funcoes_proibidas:
                if hasattr(node, 'func') and hasattr(node.func, 'id'):
                    assert node.func.id != func_name, f'Utilizou a função proibida {func_name}'

    metodos_proibidos = ['intersection', 'union', 'difference']

    source = getsource(funcoes)
    ex_ast = ast.parse(source)
    for node in ast.walk(ex_ast):
        for node_interno in ast.walk(node):
            if isinstance(node_interno, ast.Attribute) and node_interno.attr in metodos_proibidos:
                assert False, f'Utilizou o método proibido {node_interno.attr}'


def verifica_lista(esperado, obtido, msg):
    marcador = '\n' + '*' * 50 + '\n'
    for e in esperado:
        assert e in obtido, f'{marcador}O elemento {e} deveria estar na lista.\n{msg}'

    for o in obtido:
        assert o in esperado, f'{marcador}O elemento {o} não deveria estar na lista.\n{msg}'

    assert len(esperado) == len(obtido), f'{marcador}As listas deveriam ter o mesmo tamanho.\n{msg}'
    assert sorted(esperado) == sorted(obtido), f'{marcador}As listas deveriam ter os mesmos elementos. A ordem dos elementos não importa.\n{msg}'



def verifica_dicionario(esperado, obtido, msg):
    marcador = '\n' + '*' * 50 + '\n'
    for k, v in esperado.items():
        assert k in obtido, f'{marcador}A chave {k} deveria estar no dicionário.\n{msg}'
        if isinstance(v, list):
            verifica_lista(v, obtido[k], msg)
        elif isinstance(v, dict):
            verifica_dicionario(v, obtido[k], msg)
        elif isinstance(v, float) or isinstance(v, int):
            assert v == pytest.approx(obtido[k]), msg + marcador
        else:
            assert v == obtido[k], f'{marcador}O valor da chave {k} deveria ser {v}, mas foi {obtido[k]}.\n{msg}'
    for k, v in obtido.items():
        assert k in esperado, f'{marcador}A chave {k} não deveria estar no dicionário.\n{msg}'


@pytest.mark.timeout(3)
@pytest.mark.dependency_level(0)
def test_funcoes_nao_possui_prints_nem_inputs():
    source = getsource(funcoes)

    ex_ast = ast.parse(source)
    nao_tem_print = True
    nao_tem_input = True
    for node in ast.walk(ex_ast):
        if isinstance(node, ast.Call):
            try:
                if node.func.id == 'print':
                    nao_tem_print = False
                if node.func.id == 'input':
                    nao_tem_input = False
            except:
                pass
    assert nao_tem_print, f'O arquivo funcoes.py não deveria conter nenhum print'
    assert nao_tem_input, f'O arquivo funcoes.py não deveria conter nenhum input'


@pytest.mark.max_points(0)
@pytest.mark.dependency_level(2)
def test_code_quality():
    filenames = ["funcoes.py"]
    proc = subprocess.run("python3 -m edulint -o no-flake8 .".split() + filenames, capture_output=True, encoding="utf8")

    errors = {}
    lines = {}
    current_key = ""
    data = proc.stdout.splitlines()
    for line in data:
        if "*" * 15 in line:
            current_key = line.split()[1].strip()
            errors[current_key] = []
            lines[current_key] = []
        else:
            skip_file_name_idx = line.find(": ") + 2
            errcode = line[skip_file_name_idx:skip_file_name_idx+5].strip()
            line_num_idx = line.find(":")
            line_num_idx_end = line.find(":", line_num_idx+1)
            linenum = int(line[line_num_idx+1: line_num_idx_end])
            errors[current_key].append(errcode)
            lines[current_key].append(linenum)

    errors_of_interest = {
        # Quiz 1
        "W0104": "Linha não tem efeito",
        "W0127": "Variávei atribuída a si mesma",
        "E0601": "Usou variável antes de definir",
        "E0102": "Definiu duas funções com mesmo nome",

        # Quiz 2
        "R6201": "Condicional redundante: return (Padrão 1)",
        "R6203": "Condicional redundante: atribuição de booleano (Padrão 2)",
        "R1705": "if-return não precisa de else (Padrão 4)",
        "R6611": "if-elif onde if-else é suficiente (Padrão 3)",
        "R6205": "Condicional com if vazio faz o código mais difícil de ler (leitor deve negar a condição para ver quando o else executa) -- (Padrão 5) ",

        # Quiz 3
        "R6301": "Evite usar while True e terminar o loop com if + break (While Indo Além)",

        # Quiz 4
        "R6305": "Use for e range quando o número de iterações é conhecido",
        "R6604": "Não use else em for",
        "R6304": "Modificar a variável de controle no final do loop for não tem efeito. Em Python, o loop for cuida de atribuir novo valor em cada iteração.",
        
        # Quiz 5
        "R1733": "Você está usando items() e ainda acessando usando o dicionário. Reveja o Padrão 2 - Indo Além Dicionários",
        "R6101": "Não use índices para iterar em sequências quando não precisa do índice. Reveja o Padrão 1 - Indo Além Dicionários",
        "R6303": "Você está modificando a lista durante o for. Reveja o Padrão 3 - Indo Além Dicionários",
    }

    tem_erro = False
    error_msg = "\nSeu código tem os seguintes problemas de qualidade:\n\n"
    for f in filenames:
        if f in errors:
            tem_erro = False
            add_header_arquivo = True
            for errcode in errors_of_interest:
                try:
                    idx = errors[f].index(errcode)
                    if add_header_arquivo:
                        error_msg += f"********* {f} ***********\n"
                        add_header_arquivo = False
                    error_msg += f"Linha: {lines[f][idx]}: {errors_of_interest[errcode]}\n"
                    tem_erro = True
                except ValueError:
                    pass

    assert not tem_erro, error_msg

