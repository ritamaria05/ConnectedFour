import math
import random
from connected_four import create_board, is_valid, drop_piece, check_win
# Inicializa um nó da árvore MCTS
class Node:
    def __init__(self, state, parent=None):
        self.state = state #estado do jogo
        self.parent = parent #nó pai
        self.children = [] #filhos gerados
        self.visits = 0 #nr de visitas
        self.value = 0 #valor da recompensa

# verificação se nó expandiu todos os filhos possíveis
# retorna True se todos os movimentos possíveis já foram explorados
def is_fully_expanded(self):
    return len(self.children)==len(self.get_possible_moves)

# retorna melhor filho com base no seu UCT
#Parametros:
# exploration_weight : fator que controla a exploração vs exploração
def best_child(self, exploration_weight=1.41): # c = 1.41 ? ou c=1?
    return max(self.children, key=lambda child: child.uct_value(exploration_weight))

#cálculo do uct (upper confidence bound for trees)
#UCT = (valor/visitas) + (c*sqrt(log(visitas do pai))/visitas)
# c = exploration_weight, pode ser 1 ou 1.4 geralmente
#retorna um valor equilibrado 
def uct_value(self, exploration_weight):
    if self.visits==0:
        return float('inf') # garante que nós não visitados sejam explorados?
    exploitation = self.value / self.visits
    exploration = exploration_weight * math.sqrt(math.log(self.parent.visits)/self.visits)
    return exploitation + exploration

#Implementação a Função expandir:
# expande um novo filho aleatório se ainda houver movimentos possiveis
# retorna o novo nó filho criado ou None se n houver mais movimentos possíveis
def expansion(self):
    #Gerar todos os movimentos válidos a partir do estado atual
    # Criar nós filhos para cada jogada possível
    possible_moves = self.get_possible_moves()
    tried_moves = [child.state for child in self.children]
    remaining_moves = [move for move in possible_moves if move not in tried_moves]

    if not remaining_moves:
        return None # não há mais expansões possíveis

    new_state = random.choice(remaining_moves)
    child_node = Node(new_state,parent=self)
    self.children.append(child_node)
    return child_node

# retorna uma lista de estados possíveis a partir do estado atual
# as jogadas válidas são as colunas que ainda possuem espaços disponiveis
def get_possible_moves(self):
    possible_moves = []
    for col in range(len(self.state[0])):
        for row in range(len(self.state)):
            if self.state[row][col]==0: #se o estado for um espaço vazio
                new_state = [row[:]for row in self.state]
                new_state[row][col]=1
                possible_moves.append(new_state)
                break
    return possible_moves

#propaga a recompensa de volta para os nós pais
# parametro: reward, valor da recompensa a ser propagada
def backpropagation(self, reward):
    self.visits += 1
    self.value += reward
    if self.parent:
        self.parent.backpropagation(reward)

#seleciona recursivamente o melhor nó filho até alcançar um nó não expandido
# retorna o nó folha a ser expandido
def select(self):
    if not self.children:
        return self # não tem filhos
    return self.best_child().select()

#implementação de uma simulação aleatoria do jogo
#simula uma partida a partir do estado atual até ao terminal
#retorna o valor da recomepnsa para o jogador atual com base no resultado da simulação
def simulate(self):
        board = [row[:] for row in self.state]  # Copia o tabuleiro
        current_player = 'X'

        while True:
            possible_moves = [col for col in range(7) if is_valid(board, col)]
            if not possible_moves:
                return 0  # Empate

            col = random.choice(possible_moves)
            row = next(r for r in range(6) if board[r][col] == 0)
            drop_piece(board, row, col, current_player)

            if check_win(board, current_player):
                return 1 if current_player == 'X' else -1  # Vitória do jogador

            current_player = 'O' if current_player == 'X' else 'X'

