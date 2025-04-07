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

# Nova função: integra o MCTS para que a IA (jogador "O") jogue contra o utilizador ("X")
def play_game_with_mcts():
    from mcts import mcts_decision  # Importa a função mcts_decision sem alterar mcts.py
    board = create_board()
    game_over = False
    # Definindo: utilizador joga com "X" e a IA com "O"
    turn = "X"

    while not game_over:
        print_board(board)
        if turn == "X":
            try:
                col = int(input("Jogador X, escolha uma coluna (0-6): "))
            except ValueError:
                print("Jogada inválida. Digite um número entre 0 e 6.")
                continue
        else:
            print("IA está a pensar...")
            col = mcts_decision(board, iterations=50000)
            print(f"IA escolheu a coluna {col}")

        if col < 0 or col >= COLUMN_COUNT or not is_valid(board, col):
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

def play_game_mcts_vs_mcts():
    from mcts import mcts_decision  # Importa a função MCTS
    board = create_board()
    game_over = False
    turn = "X"  # Começa com "X"

    while not game_over:
        print_board(board)
        print(f"IA ({turn}) está a pensar...")

        # MCTS decide o movimento para o jogador atual
        col = mcts_decision(board, iterations=50000)
        print(f"IA ({turn}) escolheu a coluna {col}")

        if col < 0 or col >= COLUMN_COUNT or not is_valid(board, col):
            print("Jogada inválida. Isso não deveria acontecer! Reiniciando jogada.")
            continue

        row = next(r for r in range(6) if board[r][col] == 0)
        drop_piece(board, row, col, turn)

        if check_win(board, turn):
            print_board(board)
            print(f"A IA ({turn}) venceu!")
            game_over = True
        elif is_draw(board):
            print_board(board)
            print("Empate!")
            game_over = True
        else:
            turn = switch_player(turn)

if __name__ == "__main__":
    print("Escolha um modo de jogo: \n 1: Jogador vs Jogador \n 2: Jogador vs Computador \n 3: Computador vs. Computador ")
    mode = int(input("Modo: "))
    if(mode==1):
        play_game()
    elif(mode==2):
        # Para jogar contra a IA utilizando o MCTS, execute a função abaixo:
        play_game_with_mcts()
    elif(mode==3):
        play_game_mcts_vs_mcts()
    else:
        print("Modo de jogo inválido. Digite um número de 1 a 3: ")
