import math

ROW_COUNT = 6
CLUMN_COUNT = 7

# função que inicializa o tabuleiro
def create_board():
    board = [[0 for _ in range(7)] for _ in range(6)]
    return board

# função para exibir o tabuleiro no terminal de maneira mais bonitinha
def print_board(board):
    print(" 0 1 2 3 4 5 6")
    print("---------------")
    for row in reversed(board):
        print("|" + "|".join(f"{cell if cell != 0 else ' '}" for cell in row) + "|")
    print("---------------")

# verifica se a jogada é válida (entre 0 e 6)
def is_valid(board,col):
    return board[ROW_COUNT-1][col] == 0

# insere a peça na coluna do input
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Função para verificar se há win condition
def check_win(board, piece):
    # verifica horizontalmente
    for row in range(6):
        for col in range(7 - 3):
            if board[row][col] == piece and board[row][col+1] == piece and \
               board[row][col+2] == piece and board[row][col+3] == piece:
                return True
    
    # verifica verticalmente
    for col in range(7):
        for row in range(6 - 3):
            if board[row][col] == piece and board[row+1][col] == piece and \
               board[row+2][col] == piece and board[row+3][col] == piece:
                return True
    
    # verifica ambas as diagonais
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

# alterna entre turnos do X e O
def switch_player(current):
    return 'O' if current == 'X' else 'X'

# verifica se há empate
def is_draw(board):
    for col in range(7):
        if board[ROW_COUNT-1][col] == 0:
            return False
    return True

# executa o modo jogador v jogador (unico modo atual por isso é a default)
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

# Iinicia o jogo (testing feature)
if __name__ == "__main__":
    play_game()
