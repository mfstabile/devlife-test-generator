
@pytest.mark.timeout(3)
@pytest.mark.parametrize(
    '<parameters>, esperado',
    [
        pytest.param(<parameters>, esperado, id=f'test <func_name> <parameter_input>')
        for <parameters>, esperado in <tests>
    ]
)
@pytest.mark.max_points(0)
@pytest.mark.dependency_level(<dependency_level>)
def test_<level>_etapa<phase>_<func_name>(<parameters>, esperado):
    assert_<func_name>_funciona(<parameters>, esperado)


@pytest.mark.timeout(3)
@pytest.mark.parametrize(
    '<parameters>, esperado',
    [
        pytest.param(<parameters>, esperado, id=f'test <func_name> <parameter_input>')
        for <parameters>, esperado in [
            
        ]
    ]
)
@pytest.mark.max_points(0)
@pytest.mark.dependency_level(<dependency_level>)
def test_<level>_etapa<phase>_<func_name>_exemplo1(<parameters>, esperado):
    assert_<func_name>_funciona(<parameters>, esperado, exemplo = " para o exemplo 1")

