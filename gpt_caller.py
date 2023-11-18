import openai
import os
from dotenv import load_dotenv
import requests
import json

class GPTCaller:
    def __init__(self):
        self.model = "gpt-3.5-turbo-1106"
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise Exception("OPENAI_API_KEY not set on .env file")
        # Set headers
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        self.url = 'https://api.openai.com/v1/chat/completions'

    def get_tests(self, amount, function):
        messages=[
        {"role": "system", "content": "You are a code generator. You only create valid python code. Generate test cases in a concise list format without any explanations or additional comments."},
        {"role": "user", "content": """Generate 5 tests in a simple list format similar to this: [('input1',), ('input2',), ...]. Please do not include any explanations or comments for the following code:
def gera_posicoes(linha, coluna, orientacao, nome):
    navios = {
        'porta-aviões': 4,
        'navio-tanque': 3,
        'destroyer': 2,
        'submarino': 1
    }
    posicoes = [[linha, coluna]]
    if orientacao == 'horizontal':
        for i in range(1, navios[nome]):
            posicoes.append([linha, coluna + i])
    else:
        for i in range(1, navios[nome]):
            posicoes.append([linha + i, coluna])
    return posicoes
"""},
        {"role": "assistant", "content": """[
            (2, 5, 'horizontal', 'navio-tanque'),
            (6, 4, 'horizontal', 'submarino'),
            (0, 0, 'horizontal', 'porta-aviões'),
            (4, 2, 'horizontal', 'destroyer'),
            (1, 1, 'vertical', 'submarino'),
]
"""},
        {"role": "user", "content": f"""Generate {amount} tests in a simple list format similar to this: [('input1',), ('input2',), ...]. Please do not include any explanations or comments for the following code:
{function}
"""}
    ]
        # Your request payload
        data = {
            "model":self.model,
            "messages": messages
        }
        attempts = 5
        while attempts > 0:
            try:
                response = requests.post(self.url, headers=self.headers, data=json.dumps(data), timeout=60) # 60 seconds timeout
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            except requests.exceptions.Timeout:
                print("The request timed out. Retrying...")
                attempts -= 1
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                attempts -= 1
        raise Exception("Could not get response from OpenAI API.")
    
    def get_statement(self, function):
        messages=[
        {"role": "system", "content": "You are a computer science undergraduate teacher. You create statements for questions describing only the expected inputs and outputs. Pay close attention to the comments in the code and the function's parameters and return type. Ensure your explanation is concise, accurate, and adheres strictly to the provided code structure."},
        {"role": "user", "content": '''Generate a statement in Portuguese for the following python code:
def posicao_personagem(objetos: list) -> list:
    """basico
    Objetos é uma lista de dicionários no formato:
    [
        {
            "nome": "character",
            "linha": 0,
            "coluna": 0
        },
    ]
    """
    for obj in objetos:
        if obj["nome"] == "character":
            return [obj["linha"], obj["coluna"]]
'''},
        {"role": "assistant", "content": """
A função que iremos implementar deve retornar a posição do personagem do jogador.

No arquivo `funcoes.py`, implemente uma função chamada `posicao_personagem` que recebe como argumentos uma lista de dicionários contendo os elementos do jogo no formato acima. A função deve retornar uma lista de tamanho `#!python 2` posições, onde a primeira posição é a `linha` e a segunda posição é a `coluna` onde está o personagem. O personagem é sempre identificado pela string `#!python 'character'` na chave `#!python 'nome'`.

**Exemplo 1:**

```python
objetos = [
  {
    "nome": "character",
    "linha": 0,
    "coluna": 0
  },
  {
    "nome": "key",
    "linha": 2,
    "coluna": 3
  },
  {
    "nome": "exit",
    "linha": 5,
    "coluna": 7
  }
]

print(posicao_personagem(objetos))
```

**Saída:**

```
[0, 0]
```
"""},
    {"role": "user", "content": '''Generate a statement in Portuguese for the following code:
def cadastra_tentativa(caracteristica: str, valor: str, tentativas: dict) -> dict:
    """basico
    Tentativas é um dicionário no formato { 'cobertura': ['pelos'] }:
    """
    if caracteristica not in tentativas:
        tentativas[caracteristica] = [valor]
    else:
        tentativas[caracteristica].append(valor)
    return tentativas
'''},
    {"role": "assistant", "content": """
O jogo utilizará um dicionário para armazenar as características dos animais. Cada chave do dicionário é uma característica e o valor é uma lista com os valores possíveis da característica. Esse dicionário pode mudar de acordo com o jogo.

Veja um exemplo abaixo:

```python
caracteristicas = {
    'alimentacao': ['carnivoro', 'onivoro', 'herbivoro'],
    'locomocao': ['aquatico', 'terrestre', 'voador'],
    'habitat': ['terra', 'agua'],
    'mamifero': [False, True],
    'patas': [0, 2, 4, 8],
    'voa': [False, True],
    'cobertura': ['penas', 'pelos', 'escamas'],    
}
```

A tentativa do jogador consiste em escolher umas das possíveis `características` e um dos possíveis `valores` da característica. Por exemplo, o jogador pode escolher a característica `alimentacao` e o valor `carnivoro`.

Nesta primeira etapa do desenvolvimento queremos armazenar as tentavivas do jogador ao logo das rodadas. Para isso, vamos armazenar as tentativas em um dicionário onde a chave é a `característica` e o valor é uma lista com os valores da característica.

No arquivo `funcoes.py`, implemente uma função chamada `cadastra_tentativa` que recebe como argumentos uma string com a característica, uma string com o valor e um dicionário contendo as tentativas realizadas anteriormente. A função deve retornar o dicionário atualizado com o valor inserido na chave da característica.

Veja alguns exemplos abaixo:

**Exemplo 1:**

```python
caracteristica = 'cobertura'
valor = 'penas'
tentativas = { 'cobertura': ['pelos'] }
```

**Saída 1:** 
```python
{ 'cobertura': ['pelos', 'penas'] }
```
"""},
    {"role": "user", "content": f"""Generate a statement in Portuguese for the following python code. Be sure to include the function signature and mention the types of the arguments and return value and state it should be implemented in the file `funcoes.py`:
{function}
"""}
    ]
        data = {
            "model":self.model,
            "messages": messages
        }
        attempts = 5
        while attempts > 0:
            try:
                response = requests.post(self.url, headers=self.headers, data=json.dumps(data), timeout=60) # 60 seconds timeout
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            except requests.exceptions.Timeout:
                print("The request timed out. Retrying...")
                attempts -= 1
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                attempts -= 1
        raise Exception("Could not get response from OpenAI API.")