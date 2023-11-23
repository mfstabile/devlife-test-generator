
@pytest.mark.parametrize(
    '<parameters>, esperado',
    [
        pytest.param(<parameters>, esperado, id=f'test <func_name> <parameter_input>')
        for <parameters>, esperado in <tests>
    ]
)
def test_<level>_etapa<phase>_<func_name>(<parameters>, esperado):
    assert_<func_name>_funciona(<parameters>, esperado)

