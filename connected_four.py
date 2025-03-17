# código base do jogo quatro em linha no terminal
import math
# estrutura do tabuleiro

#função para inicializar o tabuleiro
def create_board():
    # representação numa matrix 6x7
    board = [[0 for _ in range(7)] for _ in range(6)]
    return board
#função para exibir o tabuleiro no terminal
def print_board(board):
    for i in range(6):
        for j in range(7):
            print(board[i][j])
        print("\n")

