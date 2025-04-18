from codes.connected_four_novo import ConnectState
from codes.mcts_novo import MCTS


def play_player_vs_ai():
    state = ConnectState()
    mcts = MCTS(state)

    while not state.game_over():
        print("Current state:")
        state.print()

        user_move = int(input("Enter a move: "))
        while user_move not in state.get_legal_moves():
            print("Illegal move")
            user_move = int(input("Enter a move: "))

        state.move(user_move)
        mcts.move(user_move)

        state.print()

        if state.game_over():
            print("Player one won!")
            break

        print("Thinking...")

        mcts.search(10)
        num_rollouts, run_time = mcts.statistics()
        print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
        move = mcts.best_move()

        print("MCTS chose move: ", move)

        state.move(move)
        mcts.move(move)

        if state.game_over():
            print("Player two won!")
            break

def play_player_vs_player():
    state = ConnectState()

    while not state.game_over():
        print("Estado atual do jogo:")
        state.print()

        print(f"Jogador {'1 (X)' if state.to_play == 1 else '2 (O)'}:")
        move = int(input("Escolha uma coluna (0-6): "))
        while move not in state.get_legal_moves():
            print("Movimento inválido. Tente novamente.")
            move = int(input("Escolha uma coluna (0-6): "))

        state.move(move)

    state.print()
    outcome = state.get_outcome()
    if outcome == 1:
        print("Jogador 1 venceu!")
    elif outcome == 2:
        print("Jogador 2 venceu!")
    else:
        print("Empate!")

def play_ai_vs_ai():
    state = ConnectState()
    mcts1 = MCTS(state)
    mcts2 = MCTS(state)

    while not state.game_over():
        print("Estado atual:")
        state.print()
        print("Pensando...")

        if state.to_play == 1:
            mcts1.search(10)
            move = mcts1.best_move()
        else:
            mcts2.search(10)
            move = mcts2.best_move()

        print(f"MCTS ({'X' if state.to_play == 1 else 'O'}) escolheu a jogada: {move}")

        state.move(move)
        mcts1.move(move)
        mcts2.move(move)

    state.print()
    outcome = state.get_outcome()
    if outcome == 1:
        print("Jogador 1 (IA) venceu!")
    elif outcome == 2:
        print("Jogador 2 (IA) venceu!")
    else:
        print("Empate!")

if __name__ == "__main__":
    print("Escolha um modo de jogo: \n 1: Jogador vs Jogador \n 2: Jogador vs Computador \n 3: Computador vs Computador \n")
    mode = int(input("Modo: "))
    if mode==1:
        play_player_vs_player()

    elif mode==2:
        play_player_vs_ai()
    
    elif mode==3:
        play_ai_vs_ai()

