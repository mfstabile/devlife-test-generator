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

def create_slots(n: int) -> list:
    """proficiente"""
    colores = ['amarelo', 'azul', 'preto', 'rosa', 'verde', 'vermelho']
    slot = []
    for number in range(1, n + 1):
        for color in colores:
            slot.append( {'number': number, 'color': color})
    return slot