#responsável por jogar várias partidas e gerar dataset

import random
import numpy as np
from mcts_novo import MCTS  # Supondo que mcts_choose_move já foi implementado
from connected_four_novo import ConnectState, GameMeta, MCTSMeta

# Função para gerar o dataset de estados e movimentos
def generate_mcts_dataset(num_games=1000):
    dataset = []  # Lista para armazenar os dados (estado, movimento)
    
    for _ in range(num_games):
        state = ConnectState()  # Cria um novo estado de jogo
        moves = []  # Lista para armazenar os movimentos e estados
        mcts = MCTS(state)
        mcts.search(time_limit=1)
        while not state.game_over():  # Enquanto o jogo não terminar
            move = mcts.best_move()  # Escolhe o próximo movimento com MCTS
            state.move(move)  # Aplica o movimento no estado atual
            moves.append((state, move))  # Armazena o estado e o movimento
        
        # Armazenar todos os movimentos e seus estados no dataset
        for s, m in moves:
            dataset.append((s.flatten(), m))  # Transforma o estado em vetor de 42 valores
    
    return dataset

# Salvar o dataset em um arquivo CSV
def save_dataset(dataset, filename='mcts_dataset.csv'):
    with open(filename, 'w') as f:
        f.write("state,move\n")
        for state, move in dataset:
            f.write(f"{' '.join(map(str, state))},{move}\n")

# Gerar e salvar o dataset
if __name__ == "__main__":
    dataset = generate_mcts_dataset(num_games=1000)  # Gerar 1000 jogos
    save_dataset(dataset)  # Salvar o dataset em arquivo CSV
