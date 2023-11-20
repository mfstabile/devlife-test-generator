
def assert_<func_name>_funciona(<parameters>, esperado, exemplo = ""):
    assert_nao_usa_funcoes_proibidas()
    assert funcoes is not None, 'Não foi possível importar o módulo funcoes. Verifique se o código não contém nenhum erro de sintaxe ou uso de input.'
    function_name = '<func_name>'
    expected_params = <expected_params>
    
    assert funcoes and <func_name>, 'A função <func_name> não foi definida no arquivo funcoes.py'
    sig = signature(funcoes.<func_name>)
    n_params = len(sig.parameters)
    assert n_params == expected_params, f'A função {function_name} deve receber {expected_params} argumentos, porém a função está recebendo {n_params}'

    marcador = '\n' + '*' * 50 + '\n'
    msg = marcador
    msg += f'Algo deu errado{exemplo}!! Para os argumentos, <parameter_input>.\nEra esperado = <expected_text>. '
    <random_text>
    try:
        obtido = funcoes.<func_name>(<params_call>)
    except Exception as e:
        msg += f'Para o cenário acima, o seu código apresentou o seguinte erro: \n\n{type(e).__name__}: {e}\n'
        assert False, msg + marcador

    msg += f'Porém, foi obtido <received_text>.'

    assert isinstance(obtido, <response_type>), f'{msg}\nEra esperado que a função retornasse <response_type_text>.' + marcador
    assert obtido == esperado, msg + marcador

