
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

