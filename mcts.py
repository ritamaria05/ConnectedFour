import math
import random
from connected_four import create_board, is_valid, drop_piece, check_win, switch_player, is_draw, ROW_COUNT, COLUMN_COUNT

class Node:
    def __init__(self, state, parent=None, move=None, player="O"):
        self.state = state       # Estado do jogo (tabuleiro)
        self.parent = parent     # Nó pai
        self.children = []       # Lista de nós filhos
        self.visits = 0          # Número de visitas
        self.value = 0           # Valor acumulado (recompensa)
        self.move = move         # Jogada que levou a este estado (coluna)
        self.player = player     # Jogador que realizou a jogada

    def get_possible_moves(self):
        moves = []
        for col in range(COLUMN_COUNT):
            if is_valid(self.state, col):
                new_state = [row[:] for row in self.state]
                row = next(r for r in range(ROW_COUNT) if new_state[r][col] == 0)
                drop_piece(new_state, row, col, self.player)
                moves.append((col, new_state))
        return moves

    def is_fully_expanded(self):
        return len(self.children) == len(self.get_possible_moves())

    def best_child(self, exploration_weight=1.41):
        return max(self.children, key=lambda child: child.uct_value(exploration_weight))

    def uct_value(self, exploration_weight):
        if self.visits == 0:
            return float('inf')
        exploitation = self.value / self.visits
        exploration = exploration_weight * math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + exploration

    def expand(self):
        possible_moves = self.get_possible_moves()
        tried_moves = [child.move for child in self.children]
        remaining_moves = [move for move, state in possible_moves if move not in tried_moves]
        if not remaining_moves:
            return None
        chosen_move = random.choice(remaining_moves)
        for move, state in possible_moves:
            if move == chosen_move:
                new_state = state
                break
        next_player = switch_player(self.player)
        child_node = Node(new_state, parent=self, move=chosen_move, player=next_player)
        self.children.append(child_node)
        return child_node

    def simulate(self):
        simulation_state = [row[:] for row in self.state]
        current_player = self.player
        while True:
            possible_moves = [col for col in range(COLUMN_COUNT) if is_valid(simulation_state, col)]
            if not possible_moves:
                return 0
            col = random.choice(possible_moves)
            row = next(r for r in range(ROW_COUNT) if simulation_state[r][col] == 0)
            drop_piece(simulation_state, row, col, current_player)
            if check_win(simulation_state, current_player):
                return 1 if current_player == "O" else -1
            current_player = switch_player(current_player)

    def backpropagate(self, reward):
        self.visits += 1
        self.value += reward
        if self.parent:
            self.parent.backpropagate(reward)

def mcts_decision(state, iterations=1000):
    root = Node(state, player="O")
    for _ in range(iterations):
        node = root
        while node.children and node.is_fully_expanded():
            node = node.best_child()
        if not check_win(node.state, switch_player(node.player)) and not is_draw(node.state):
            child = node.expand()
            if child:
                node = child
        reward = node.simulate()
        node.backpropagate(reward)
    best = root.best_child(exploration_weight=0)
    return best.move
