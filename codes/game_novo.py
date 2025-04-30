from connected_four_novo import ConnectState  # Representa o estado do jogo
from mcts_novo import MCTS                   # Implementa o algoritmo MCTS

# Exceções específicas para controlo de fluxo

class RestartGameException(Exception):
    pass

class QuitGameException(Exception):
    pass


# Leitura de inteiro seguro
def safe_int_input(prompt):
    while True:
        try:
            value = input(prompt)
            if value.lower() == 'restart':
                raise RestartGameException
            if value.lower() == 'quit':
                raise QuitGameException
            return int(value)
        except ValueError:
            print("Entrada inválida. Por favor insira um número inteiro.")
        except EOFError:
            raise

# Leitura de jogada com reinício/saída
def safe_move_input(state, prompt="Escolha uma coluna (0-6), 'restart' ou 'quit': "):
    while True:
        try:
            user_input = input(prompt)
            if user_input.lower() == 'restart':
                raise RestartGameException
            if user_input.lower() == 'quit':
                raise QuitGameException
            move = int(user_input)
            if move in state.get_legal_moves():
                return move
            print("Movimento inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Insira um número de 0 a 6.")
        except EOFError:
            raise

# Funções de jogo com retorno de resultado

def play_player_vs_player(starting_player):
    state = ConnectState()
    state.to_play = starting_player
    while not state.game_over():
        state.print()
        print(f"Vez de {'X' if state.to_play==1 else 'O'}")
        move = safe_move_input(state)
        state.move(move)
    state.print()
    return state.get_outcome()


def play_player_vs_ai(player_piece, first):
    state = ConnectState()
    ai_piece = 2 if player_piece == 1 else 1
    mcts = MCTS(state)
    if first == 'ai':
        state.to_play = ai_piece
        state.print()
        print("Computador começando...")
        mcts.search(10)
        mv = mcts.best_move()
        print(f"MCTS ({'X' if ai_piece==1 else 'O'}) escolheu: {mv}")
        state.move(mv)
        mcts.move(mv)
    else:
        state.to_play = player_piece
    while not state.game_over():
        state.print()
        if state.to_play == player_piece:
            mv = safe_move_input(state)
            state.move(mv)
            mcts.move(mv)
        else:
            print("Computador pensando...")
            mcts.search(10)
            mv = mcts.best_move()
            print(f"MCTS ({'X' if ai_piece==1 else 'O'}) escolheu: {mv}")
            state.move(mv)
            mcts.move(mv)
    state.print()
    return state.get_outcome()


def play_ai_vs_ai(starting_player):
    state = ConnectState()
    state.to_play = starting_player
    mcts1, mcts2 = MCTS(state), MCTS(state)
    while not state.game_over():
        state.print()
        # Indica qual IA está a jogar
        current_ai = 'X' if state.to_play == 1 else 'O'
        print(f"IA {current_ai} a pensar...")
        # Execução MCTS conforme a peça
        if state.to_play == 1:
            mcts1.search(10)
            mv = mcts1.best_move()
        else:
            mcts2.search(10)
            mv = mcts2.best_move()
        # Mostra a jogada escolhida
        print(f"IA {current_ai} escolheu a coluna: {mv}")
        # Aplica a jogada e atualiza ambas as árvores
        state.move(mv)
        mcts1.move(mv)
        mcts2.move(mv)
    state.print()
    return state.get_outcome()

# Menu pós-jogo: Play Again, Change Modes, Quit
def post_game_menu():
    print("O que deseja fazer a seguir?")
    print("1: Jogar novamente")
    print("2: Mudar modo")
    print("3: Sair")
    choice = safe_int_input("Escolha: ")
    if choice == 1:
        return 'again'
    if choice == 2:
        raise RestartGameException
    return 'quit'

# Bloco principal

def main():
    x_wins = o_wins = draws = 0
    try:
        while True:
            print("1: Jogador vs Jogador\n2: Jogador vs AI\n3: AI vs AI")
            mode = safe_int_input("Modo: ")
            # Definições iniciais do modo
            if mode == 1:
                print("Quem começa? \n1: X  \n2: O")
                first = 1 if safe_int_input("Escolha: ")==1 else 2
                while True:
                    outcome = play_player_vs_player(first)
                    if outcome == 1: x_wins += 1
                    elif outcome == 2: o_wins += 1
                    else: draws += 1
                    print(f"Placar: (X) {x_wins} - {o_wins} (O) (Empates: {draws})")
                    action = post_game_menu()
                    if action == 'again':
                        continue
                    elif action == 'quit':
                        raise QuitGameException
            elif mode == 2:
                print("Quem começa? \n1: Jogador  \n2: AI")
                first = 'player' if safe_int_input("Escolha: ")==1 else 'ai'
                print("Que peça preferes? \n1: X  \n2: O")
                piece = 1 if safe_int_input("Escolha: ")==1 else 2
                while True:
                    outcome = play_player_vs_ai(piece, first)
                    if outcome == piece: x_wins += 1
                    elif outcome != piece: o_wins += 1
                    print(f"Placar: (Jogador) {x_wins if piece==1 else o_wins} - {o_wins if piece==1 else x_wins} (AI)")
                    action = post_game_menu()
                    if action == 'again':
                        continue
                    elif action == 'quit':
                        raise QuitGameException
            elif mode == 3:
                print("Quem começa? \n1: X  \n2: O")
                first = 1 if safe_int_input("Escolha: ")==1 else 2
                while True:
                    outcome = play_ai_vs_ai(first)
                    if outcome == 1: x_wins += 1
                    elif outcome == 2: o_wins += 1
                    else: draws += 1
                    print(f"Placar: (X) {x_wins} - {o_wins} (O) (Empates: {draws})")
                    action = post_game_menu()
                    if action == 'again':
                        continue
                    elif action == 'quit':
                        raise QuitGameException
            else:
                print("Modo inválido.")
    except RestartGameException:
        print("Mudando modo...")
        main()
    except QuitGameException:
        print("Programa encerrado.")
    except EOFError:
        print("Entrada finalizada.")

if __name__ == "__main__":
    main()
# Este código implementa um jogo de Conecta 4 com várias opções de modo de jogo.