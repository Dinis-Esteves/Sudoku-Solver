from sys import stdin
from search import Problem, Node, depth_first_graph_search

class SudokuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = SudokuState.state_id
        SudokuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

class Board:
    """Classe que representa o tabuleiro do Sudoku."""
    def __init__(self, matrix):
        self.matrix = matrix    

    def get_line(self, line: int) -> list:
        """Retorna um conjunto com os valores da linha especificada."""
        return self.matrix[line]
    
    def get_column(self, column: int) -> list:
        """Retorna um conjunto com os valores da coluna especificada."""
        return [self.matrix[i][column] for i in range(9)]

    def get_square(self, square: int) -> list:
        """Retorna um conjunto com os valores do quadrado especificado.
        O quadrado é identificado pelo número de 0 a 8, onde:
        0-2: primeira linha, 3-5: segunda linha, 6-8: terceira linha.
        """
        start_row = (square // 3) * 3
        start_col = (square % 3) * 3
        return [self.matrix[i][j] for i in range(start_row, start_row + 3)
                for j in range(start_col, start_col + 3)]
    
    def write_number(self, number:int, coords: tuple) -> None:
        """Escreve o número especificado na posição indicada por coords."""
        row, col = coords
        self.matrix[row][col] = str(number)

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        matrix = []
        line = stdin.readline().split()

        while line:
            matrix.append(line)
            line = stdin.readline().split()

        # initializes the board
        board = Board(matrix)
        return board

    def __str__(self):
        """representção textual de um sudoku"""
        linhas = []
        
        def get_cell(val):
            return f" {val} " if val != "x" else " x "

        topo =    "┌" + ("─" * 9 + "┬") * 2 + "─" * 9 + "┐"
        meio =    "├" + ("─" * 9 + "┼") * 2 + "─" * 9 + "┤"
        fundo =   "└" + ("─" * 9 + "┴") * 2 + "─" * 9 + "┘"

        linhas.append(topo)
        for i in range(9):
            linha = "│"
            for j in range(9):
                val = self.matrix[i][j]
                linha += get_cell(val)
                if (j + 1) % 3 == 0:
                    linha += "│"
            linhas.append(linha)
            if (i + 1) % 3 == 0 and i != 8:
                linhas.append(meio)
        linhas.append(fundo)

        return "\n".join(linhas)
    
    def copy(self):
        new_matrix = [self.matrix[i][:] for i in range(9)] 
        return Board(new_matrix)

class Sudoku(Problem):
    def __init__(self, initial: SudokuState):
        """O construtor especifica o estado inicial."""
        self.initial = initial

    def actions(self, state: SudokuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        for i in range(9):
            for j in range(9):
                if state.board.matrix[i][j] == "x":
                    has_action = False
                    # Ações possíveis são os números de 1 a 9
                    
                    for number in range(1, 10):
                        number = str(number)
                        if (number not in state.board.get_line(i) and
                                number not in state.board.get_column(j) and
                                number not in state.board.get_square((i // 3) * 3 + j // 3)):
                            actions.append((i, j, number))
                            has_action = True
                    if not has_action:
                        return []  # Se não houver ações possíveis para uma celula, mata o estado
        return actions

    def result(self, state: SudokuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        row, col, number = action
        new_board = state.board.copy()
        new_board.write_number(number, (row, col))
        return SudokuState(new_board)

    def goal_test(self, state: SudokuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        print(state.board)
        for i in range(9):
            line = set(state.board.get_line(i))
            column = set(state.board.get_column(i))
            square = set(state.board.get_square(i))
            if 'x' in line or len(line) != 9:
                return False
            if 'x' in column or len(column) != 9:
                return False    
            if 'x' in square or len(square) != 9:
                return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

def main():
    board = Board.parse_instance()
    problem = Sudoku(SudokuState(board))
    print("Sudoku inicial:\n")
    print(board)
    print("Resolvendo o Sudoku...\n")
    Solution = depth_first_graph_search(problem)
    if Solution is None:
        print("Não foi possível resolver o Sudoku.")
    else:
        print("Sudoku resolvido:\n")
        print(Solution.state.board) 

if __name__ == "__main__":
    main()
