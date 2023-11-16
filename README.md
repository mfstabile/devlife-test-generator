# devlife-test-generator
This project aims to improve the process of creating pytests for the Developer Life course at Insper by using AI.

## Executing the project

When you are first running the project, install the dependencies with:

    $ pip install -r requirements.txt

### Generate the tests

To generate the tests file, run:

    $ python generate_tests.py <input_file>

The input file is a python file containing the functions to be tested. Example:

    $ python generate_tests.py input.py

There are two optional arguments. The first one enables the GPT model to automatically generate the test scenarios. The second one dictates the amount of scenarios to be generated. Example:

    $ python generate_tests.py input.py -gpt 10

If not passed, the default value for the number of scenarios is 5.

*The tests will be generated in the `tests_.py` file. This file will be overwritten if it already exists.*

### Generate the statements

To generate the statements files, run:

    $ python generate_statements.py <input_file> <test_name>

*The statements will be generated in the `<test_name>` folder, one file per difficulty level. These files will be overwritten if they already exist.*

## Structure of the code

There are a few restrictions on the functions code that must be obeyed.

 - All parameters types and the return type must be annotated in the function.
 - The first line of the Docstring must dictate the level of the exercise.

Example:

```python
def find_line_and_column(board: list, number: int, color: str) -> list:
    """basico
    color must be one of the following: "blue", "red", "green".
    number must be an integer between 1 and 6.
    """
    for i_line in range(len(board)):
        for i_column in range(len(board[i_line])):
            if board[i_line][i_column] == {'number': number, 'color': color}:
                return [i_line, i_column]
    return [-1, -1]
```

## Environment Variables

If you wish to use the GPT model to automatically generate the test scenarios, you need to fill the following variable:

- `OPENAI_API_KEY`: API key for the OpenAI API.
