
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
