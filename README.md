# devlife-test-generator
This project aims to improve the process of creating pytests for the Developer Life course at Insper by using AI.

## Executing the project

When you are first running the project, install the dependencies with:

    $ pip install -r requirements.txt

Then, to execute the project, run:

    $ python generate_tests.py <input_file>

The input file is a python file containing the functions to be tested. Example:

    $ python generate_tests.py input.py

There are two optional arguments. The first one enables the GPT model to automatically generate the test scenarios. The second one dictates the amount of scenarios to be generated. Example:

    $ python generate_tests.py input.py -gpt 10

If not passed, the default value for the number of scenarios is 5.

*The tests will be generated in the `tests_.py` file. This file will be overwritten if it already exists.*

## Structure of the code

There are a few restrictions on the functions code that must be obeyed.

 - All parameters types and the return type must be annotated in the function.
 - The first line of the Docstring must dictate the level of the exercise.

Example:

```python
def encontra_linha_e_coluna(tabuleiro: list, numero: int, cor: str) -> list:
    """basico"""
    for i_linha in range(len(tabuleiro)):
        for i_coluna in range(len(tabuleiro[i_linha])):
            if tabuleiro[i_linha][i_coluna] == {'numero': numero, 'cor': cor}:
                return [i_linha, i_coluna]
    return [-1, -1]
```

## Environment Variables

If you wish to use the GPT model to automatically generate the test scenarios, you need to fill the following variable:

- `OPENAI_API_KEY`: API key for the OpenAI API.
