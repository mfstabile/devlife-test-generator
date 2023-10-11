
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
