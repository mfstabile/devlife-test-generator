import openai
import os
from dotenv import load_dotenv

class GPTCaller:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise Exception("OPENAI_API_KEY not set on .env file")
        openai.api_key = api_key

    def get_tests(self, amount, function):
        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a code generator. You only create valid python code."},
        {"role": "user", "content": """Generate 5 tests for the following code:
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
        {"role": "user", "content": f"""Generate {amount} tests for the following code:
{function}
"""}
    ],)
        return response.choices[0].message.content