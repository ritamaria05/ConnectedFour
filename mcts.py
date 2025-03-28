import math

ROW_COUNT = 6
COLUMN_COUNT = 7

# Função que inicializa o tabuleiro
def create_board():
    board = [[0 for _ in range(7)] for _ in range(6)]
    return board

# Função para exibir o tabuleiro no terminal de maneira mais bonitinha
def print_board(board):
    print(" 0 1 2 3 4 5 6")
    print("---------------")
    for row in reversed(board):
        print("|" + "|".join(f"{cell if cell != 0 else ' '}" for cell in row) + "|")
    print("---------------")

# Verifica se a jogada é válida (entre 0 e 6)
def is_valid(board, col):
    return board[ROW_COUNT-1][col] == 0

# Insere a peça na coluna do input
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Função para verificar se há win condition
def check_win(board, piece):
    # Verifica horizontalmente
    for row in range(6):
        for col in range(7 - 3):
            if board[row][col] == piece and board[row][col+1] == piece and \
               board[row][col+2] == piece and board[row][col+3] == piece:
                return True

    # Verifica verticalmente
    for col in range(7):
        for row in range(6 - 3):
            if board[row][col] == piece and board[row+1][col] == piece and \
               board[row+2][col] == piece and board[row+3][col] == piece:
                return True

    # Verifica ambas as diagonais
    for row in range(3, 6):
        for col in range(7 - 3):
            if board[row][col] == piece and board[row-1][col+1] == piece and \
               board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True

    for row in range(6 - 3):
        for col in range(7 - 3):
            if board[row][col] == piece and board[row+1][col+1] == piece and \
               board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True

    return False

# Alterna entre turnos do X e O
def switch_player(current):
    return 'O' if current == 'X' else 'X'

# Verifica se há empate
def is_draw(board):
    for col in range(7):
        if board[ROW_COUNT-1][col] == 0:
            return False
    return True

# Executa o modo jogador vs jogador (único modo atual)
def play_game():
    board = create_board()
    game_over = False
    turn = 'X'

    while not game_over:
        print_board(board)
        col = int(input(f"Jogador {turn}, escolha uma coluna (0-6): "))
        if col < 0 or col >= 7 or not is_valid(board, col):
            print("Jogada inválida. Tente novamente.")
            continue

        row = next(r for r in range(6) if board[r][col] == 0)
        drop_piece(board, row, col, turn)

        if check_win(board, turn):
            print_board(board)
            print(f"Jogador {turn} venceu!")
            game_over = True
        elif is_draw(board):
            print_board(board)
            print("Empate!")
            game_over = True
        else:
            turn = switch_player(turn)

#############################################
# Funções novas para a integração da IA vs. IA
#############################################

# Função auxiliar para inverter as peças do tabuleiro.
# Troca "X" por "O" e "O" por "X". Assim, podemos usar a função mcts_decision,
# que sempre trabalha com o jogador "O", também para o jogador "X".
def swap_board(board):
    swapped = []
    for row in board:
        new_row = []
        for cell in row:
            if cell == "X":
                new_row.append("O")
            elif cell == "O":
                new_row.append("X")
            else:
                new_row.append(cell)
        swapped.append(new_row)
    return swapped

# Função para que a IA jogue contra a IA.
# Para o jogador "O", utiliza mcts_decision diretamente;
# para o jogador "X", utiliza swap_board para "enganar" a mcts_decision.
def play_game_ai_vs_ai():
    x=0
    o=0
    from mcts import mcts_decision  # Importa a função mcts_decision do ficheiro mcts.py
    board = create_board()
    game_over = False
    # Ambos os jogadores são IA: "X" e "O"
    turn = "X"

    while not game_over:
        print_board(board)
        if turn == "X":
            # Inverte o tabuleiro para que a mcts_decision (que trabalha com "O") possa decidir para "X"
            swapped = swap_board(board)
            col = mcts_decision(swapped, iterations=1000)
            print(f"IA (X) escolheu a coluna {col}")
        else:
            col = mcts_decision(board, iterations=1000)
            print(f"IA (O) escolheu a coluna {col}")

        if col < 0 or col >= COLUMN_COUNT or not is_valid(board, col):
            print("Jogada inválida. Tente novamente.")
            continue

        row = next(r for r in range(6) if board[r][col] == 0)
        drop_piece(board, row, col, turn)

        if check_win(board, turn):
            print_board(board)
            print(f"Jogador {turn} venceu!")
            if turn=="X":
                return 0
            else: return 1
            game_over = True
        elif is_draw(board):
            print_board(board)
            print("Empate!")
            game_over = True
            return 2
        else:
            turn = switch_player(turn)

#############################################
# Execução principal
#############################################
if __name__ == "__main__":
    # Para jogar contra a IA (humano vs IA), chame play_game_with_mcts()
    # Para IA vs IA, chame play_game_ai_vs_ai()
    x = 0
    o = 0
    for i in range (100):
        play_game_ai_vs_ai()
        if play_game_ai_vs_ai()==0:
            x=x+1
        else:
            if play_game_ai_vs_ai()==2:
                o=o+1
    print(f"X ganhou {x} vezes")
    print(f"O ganhou {o} vezes")
