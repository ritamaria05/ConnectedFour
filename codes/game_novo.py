from connected_four_novo import ConnectState
from mcts_novo import MCTS


class RestartGameException(Exception):
    pass

class QuitGameException(Exception):
    pass


def safe_int_input(prompt):
    try:
        return int(input(prompt))
    except EOFError:
        raise EOFError
    except ValueError:
        print("Entrada inválida. Por favor insira um número inteiro.")
        return safe_int_input(prompt)


def safe_input_with_restart_or_quit(prompt):
    user_input = input(prompt)
    if user_input.lower() == 'restart':
        raise RestartGameException("Jogo reiniciado pelo usuário.")
    elif user_input.lower() == 'quit':
        raise QuitGameException("Jogo encerrado pelo usuário.")
    return user_input


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
    
    def user_vs_tree():
        #usar arvore + novos exemplos (classify), predict move function
        pass

    def play_user_vs_tree():
        pass


def safe_input_with_restart_or_quit(prompt):
    user_input = input(prompt)
    if user_input.lower() == 'restart':
        raise RestartGameException("Jogo reiniciado pelo usuário.")
    elif user_input.lower() == 'quit':
        raise QuitGameException("Jogo encerrado pelo usuário.")
    return user_input


if __name__ == "__main__":
    x_wins = 0
    o_wins = 0
    draws = 0

    print("Escolha um modo de jogo: \n 1: Jogador vs Jogador \n 2: Jogador vs Computador \n 3: Computador vs Computador \n")
    try:
        mode = safe_int_input("Modo: ")
    except EOFError:
        print("\nEntrada finalizada. Programa encerrado.")
        exit()

    if mode in [1, 2]:
        try:
            while True:
                try:
                    print("\nQuem começa? (1: X, 2: O)")
                    first_player = safe_int_input("Escolha: ")
                    while first_player not in [1, 2]:
                        print("Escolha inválida.")
                        first_player = safe_int_input("Escolha (1: X, 2: O): ")
                except EOFError:
                    print("\nEntrada finalizada. Programa encerrado.")
                    break

                state = ConnectState()
                if first_player == 2:
                    state.to_play = 2

                if mode == 1:
                    # PvP com print jogada a jogada
                    while not state.game_over():
                        print("Estado atual do jogo:")
                        state.print()
                        print(f"Jogador {'1 (X)' if state.to_play == 1 else '2 (O)'}:")
                        try:
                            move = safe_input_with_restart_or_quit("Escolha uma coluna (0-6), 'restart' para reiniciar o jogo ou 'quit' para encerrar o jogo: ")
                            if move.lower() == 'restart':
                                raise RestartGameException("Jogo reiniciado pelo usuário.")
                            elif move.lower() == 'quit':
                                raise QuitGameException("Jogo encerrado pelo usuário.")
                            move = int(move)
                        except RestartGameException:
                            print("\nReiniciando o jogo...\n")
                            break
                        except QuitGameException:
                            print("\nSaindo do jogo...")
                            print(f'\nResultado final: "X" {x_wins}-{o_wins} "O" (Empates: {draws})\n')
                            exit()
                        except EOFError:
                            print("\nEntrada finalizada. Jogo interrompido.")
                            break
                        while move not in state.get_legal_moves():
                            print("Movimento inválido. Tente novamente.")
                            try:
                                move = safe_input_with_restart_or_quit("Escolha uma coluna (0-6), 'restart' para reiniciar o jogo ou 'quit' para encerrar o jogo: ")
                                if move.lower() == 'restart':
                                    raise RestartGameException("Jogo reiniciado pelo usuário.")
                                elif move.lower() == 'quit':
                                    raise QuitGameException("Jogo encerrado pelo usuário.")
                                move = int(move)
                            except RestartGameException:
                                print("\nReiniciando o jogo...\n")
                                break
                            except QuitGameException:
                                print("\nSaindo do jogo...")
                                print(f'\nResultado final: "X" {x_wins}-{o_wins} "O" (Empates: {draws})\n')
                                exit()
                            except EOFError:
                                print("\nEntrada finalizada. Jogo interrompido.")
                                break
                        state.move(move)
                        state.print()

                elif mode == 2:
                    mcts = MCTS(state)
                    if first_player == 2:
                        print("Computador começa...")
                        mcts.search(8)
                        move = mcts.best_move()
                        print(f"MCTS (X) escolheu: {move}")
                        state.move(move)
                        mcts.move(move)
                        state.print()

                    while not state.game_over():
                        print("Estado atual do jogo:")
                        state.print()

                        try:
                            user_move = safe_input_with_restart_or_quit("Escolha uma coluna (0-6), 'restart' para reiniciar o jogo ou 'quit' para encerrar o jogo: ")
                            if user_move.lower() == 'restart':
                                raise RestartGameException("Jogo reiniciado pelo usuário.")
                            elif user_move.lower() == 'quit':
                                raise QuitGameException("Jogo encerrado pelo usuário.")
                            user_move = int(user_move)
                        except RestartGameException:
                            print("\nReiniciando o jogo...\n")
                            break
                        except QuitGameException:
                            print("\nSaindo do jogo...")
                            print(f'\nResultado final: "X" {x_wins}-{o_wins} "O" (Empates: {draws})\n')
                            exit()
                        except EOFError:
                            print("\nEntrada finalizada. Jogo interrompido.")
                            break
                        while user_move not in state.get_legal_moves():
                            print("Movimento inválido. Tente novamente.")
                            try:
                                user_move = safe_input_with_restart_or_quit("Escolha uma coluna (0-6), 'restart' para reiniciar o jogo ou 'quit' para encerrar o jogo: ")
                                if user_move.lower() == 'restart':
                                    raise RestartGameException("Jogo reiniciado pelo usuário.")
                                elif user_move.lower() == 'quit':
                                    raise QuitGameException("Jogo encerrado pelo usuário.")
                                user_move = int(user_move)
                            except RestartGameException:
                                print("\nReiniciando o jogo...\n")
                                break
                            except QuitGameException:
                                print("\nSaindo do jogo...")
                                print(f'\nResultado final: "X" {x_wins}-{o_wins} "O" (Empates: {draws})\n')
                                exit()
                            except EOFError:
                                print("\nEntrada finalizada. Jogo interrompido.")
                                break

                        state.move(user_move)
                        mcts.move(user_move)
                        state.print()

                        if state.game_over():
                            break

                        print("Computador a pensar...")
                        mcts.search(8)
                        move = mcts.best_move()
                        print(f"MCTS (O) escolheu: {move}")
                        state.move(move)
                        mcts.move(move)
                        state.print()

                if state.game_over():
                    outcome = state.get_outcome()
                    if outcome == 1:
                        x_wins += 1
                        print('"X" venceu!')
                    elif outcome == 2:
                        o_wins += 1
                        print('"O" venceu!')
                    else:
                        draws += 1
                        print("Empate!")

                    print(f'\nResultado atual: "X" {x_wins}-{o_wins} "O" (Empates: {draws})\n')

        except QuitGameException:
            print("\nSaindo do jogo...")
            print(f'\nResultado final: "X" {x_wins}-{o_wins} "O" (Empates: {draws})\n')
        except EOFError:
            print("\nFim dos jogos.")

    elif mode == 3:
        try:
            num_games = safe_int_input("Quantos jogos deseja que a IA jogue? ")
        except EOFError:
            print("\nEntrada finalizada. Programa encerrado.")
            exit()

        for i in range(num_games):
            print(f"\n=== Jogo {i+1} ===")
            state = ConnectState()
            mcts1 = MCTS(state)
            mcts2 = MCTS(state)

            while not state.game_over():
                state.print()
                print("IA a pensar...")
                if state.to_play == 1:
                    mcts1.search(10)
                    move = mcts1.best_move()
                else:
                    mcts2.search(10)
                    move = mcts2.best_move()
                print(f"Jogador {'1 (X)' if state.to_play == 1 else '2 (O)'} escolheu: {move}")
                state.move(move)
                mcts1.move(move)
                mcts2.move(move)

            state.print()
            outcome = state.get_outcome()
            if outcome == 1:
                x_wins += 1
                print("Jogador 1 (IA - X) venceu!")
            elif outcome == 2:
                o_wins += 1
                print("Jogador 2 (IA - O) venceu!")
            else:
                draws += 1
                print("Empate!")

            print(f'Resultado atual: "X" {x_wins}-{o_wins} "O" (Empates: {draws})\n')
