def seleciona_candidatos(candidatos: list, criterios: list) -> list:
    "ex"
    selecao = []
    for c in candidatos:
        if len(c[2]) == 3 and c[2][0] >= criterios[0] and c[2][1] >= criterios[1] and c[2][2] >= criterios[2]:
            selecao.append([c[0], c[1]])
    return selecao


import copy
import random

nomes = ['Ana', 'Bruna', 'Claudia', 'Luiz', 'Pedro', 'Hamilton', 'Zeca', 'José', 'Ellen']
for n in range(10):
    criterios = [random.uniform(5.0, 10.0), random.uniform(5.0, 10.0), random.uniform(5.0, 10.0)]
    candidatos = []
    qt_candidatos = random.randint(0,15)
    for j in range(qt_candidatos):
        nome = random.choice(nomes) + ' ' + chr(random.randint(ord('A'), ord('Z'))) + '.'
        rg = '{0}-{1}'.format(random.randint(1000, 9999), random.randint(0, 9))
        notas = []
        if random.uniform(0.0, 1.0) < 0.2:
            qt_notas = random.randint(0,8)
        else:
            qt_notas = 3
        for i in range(3):
            if random.uniform(0.0, 1.0) > 0.13:
                nota = random.uniform(criterios[i], 10.0)
            else:
                nota = random.uniform(0.0, criterios[i])
            notas.append(nota)
        candidato = [nome, rg, notas]
        candidatos.append(candidato)

        esperado = seleciona_candidatos(copy.deepcopy(candidatos), criterios.copy())
        print(f'            ({candidatos}, {criterios}, {esperado}),')