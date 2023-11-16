import ast

class RandomCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.found_random_call = False

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id == 'random':  # Check if the function is from random module
                self.found_random_call = True
                return
        self.generic_visit(node)  # Continue to next node