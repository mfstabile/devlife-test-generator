def encontra_linha_e_coluna(tabuleiro: list, numero: int, cor: str) -> list:
    """basico"""
    for i_linha in range(len(tabuleiro)):
        for i_coluna in range(len(tabuleiro[i_linha])):
            if tabuleiro[i_linha][i_coluna] == {'numero': numero, 'cor': cor}:
                return [i_linha, i_coluna]
    return [-1, -1]

def cria_pecas(n: int) -> list:
    """proficiente"""
    cores = ['amarelo', 'azul', 'preto', 'rosa', 'verde', 'vermelho']
    casas = []
    for numero in range(1, n + 1):
        for cor in cores:
            casas.append( {'numero': numero, 'cor': cor})
    return casas