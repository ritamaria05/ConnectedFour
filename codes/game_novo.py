from connected_four_novo import ConnectState  # Importa a classe que representa o estado do jogo
from mcts_novo import MCTS  # Importa a classe que implementa o algoritmo MCTS (Monte Carlo Tree Search)

# Define exceções específicas para controlo de fluxo: reiniciar ou terminar o jogo
class RestartGameException(Exception):
    pass

class QuitGameException(Exception):
    pass

# Função que tenta ler um número inteiro do utilizador de forma segura
def safe_int_input(prompt):
    try:
        return int(input(prompt))  # Tenta converter o input para inteiro
    except EOFError:
        raise EOFError  # Permite o utilizador terminar com Ctrl+D
    except ValueError:
        # Se o input não for um número inteiro válido
        print("Entrada inválida. Por favor insira um número inteiro.")
        return safe_int_input(prompt)  # Repete até o utilizador inserir corretamente

# Função que lê input e verifica se o utilizador quer reiniciar ou sair do jogo
def safe_input_with_restart_or_quit(prompt):
    user_input = input(prompt)
    if user_input.lower() == 'restart':
        raise RestartGameException("Jogo reiniciado pelo utilizador.")  # Atira exceção para reiniciar
    elif user_input.lower() == 'quit':
        raise QuitGameException("Jogo encerrado pelo utilizador.")  # Atira exceção para sair
    return user_input  # Retorna input normal se for válido

# Função principal para Jogador vs Computador
def play_player_vs_ai():
    state = ConnectState()  # Inicializa o tabuleiro de jogo vazio
    mcts = MCTS(state)      # Inicializa o MCTS baseado no estado atual

    while not state.game_over():  # Continua enquanto o jogo não terminar
        print("Current state:")
        state.print()  # Mostra o tabuleiro

        # Jogador humano faz a jogada
        user_move = int(input("Enter a move: "))
        while user_move not in state.get_legal_moves():  # Garante jogada válida
            print("Illegal move")
            user_move = int(input("Enter a move: "))

        # Aplica a jogada do humano no estado
        state.move(user_move)
        mcts.move(user_move)  # Atualiza também a árvore do MCTS
        state.print()  # Mostra tabuleiro após jogada

        if state.game_over():  # Verifica se alguém ganhou ou houve empate
            print("Player one won!")
            break

        print("Thinking...")  # Computador pensa...

        # O computador usa MCTS para procurar o melhor movimento
        mcts.search(10)  # Faz 10 iterações de pesquisa MCTS
        num_rollouts, run_time = mcts.statistics()  # Mostra estatísticas de pesquisa
        print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
        move = mcts.best_move()  # Escolhe o melhor movimento encontrado

        print("MCTS chose move: ", move)

        state.move(move)  # Computador joga
        mcts.move(move)   # Atualiza árvore do MCTS

        if state.game_over():
            print("Player two won!")  # Se o computador ganhar
            break

# Função principal para Jogador vs Jogador
def play_player_vs_player():
    state = ConnectState()  # Novo jogo

    while not state.game_over():
        print("Estado atual do jogo:")
        state.print()

        print(f"Jogador {'1 (X)' if state.to_play == 1 else '2 (O)'}:")  # Indica quem joga
        move = int(input("Escolha uma coluna (0-6): "))
        while move not in state.get_legal_moves():  # Verifica jogada válida
            print("Movimento inválido. Tente novamente.")
            move = int(input("Escolha uma coluna (0-6): "))

        state.move(move)  # Aplica a jogada

    state.print()  # Mostra o tabuleiro final
    outcome = state.get_outcome()  # Verifica vencedor ou empate
    if outcome == 1:
        print("Jogador 1 venceu!")
    elif outcome == 2:
        print("Jogador 2 venceu!")
    else:
        print("Empate!")

# Função para Computador vs Computador
def play_ai_vs_ai():
    state = ConnectState()
    mcts1 = MCTS(state)  # MCTS para o primeiro jogador
    mcts2 = MCTS(state)  # MCTS para o segundo jogador

    while not state.game_over():
        print("Estado atual:")
        state.print()
        print("Pensando...")

        # IA joga consoante o turno atual
        if state.to_play == 1:
            mcts1.search(10)
            move = mcts1.best_move()
        else:
            mcts2.search(10)
            move = mcts2.best_move()

        print(f"MCTS ({'X' if state.to_play == 1 else 'O'}) escolheu a jogada: {move}")

        state.move(move)  # Aplica jogada
        mcts1.move(move)  # Atualiza árvore do MCTS para IA 1
        mcts2.move(move)  # Atualiza árvore do MCTS para IA 2

    state.print()
    outcome = state.get_outcome()
    if outcome == 1:
        print("Jogador 1 (IA) venceu!")
    elif outcome == 2:
        print("Jogador 2 (IA) venceu!")
    else:
        print("Empate!")

# Repete a função de input seguro (deve ser corrigido depois para evitar duplicação)
def safe_input_with_restart_or_quit(prompt):
    user_input = input(prompt)
    if user_input.lower() == 'restart':
        raise RestartGameException("Jogo reiniciado pelo utilizador.")
    elif user_input.lower() == 'quit':
        raise QuitGameException("Jogo encerrado pelo utilizador.")
    return user_input

# --- Bloco principal de execução ---
if __name__ == "__main__":
    x_wins = 0  # Contador de vitórias do jogador X
    o_wins = 0  # Contador de vitórias do jogador O
    draws = 0   # Contador de empates

    # Pergunta ao utilizador qual modo de jogo deseja
    print("Escolha um modo de jogo: \n 1: Jogador vs Jogador \n 2: Jogador vs Computador \n 3: Computador vs Computador \n")
    try:
        mode = safe_int_input("Modo: ")
    except EOFError:
        print("\nEntrada finalizada. Programa encerrado.")
        exit()

    # Se escolher modo Jogador vs Jogador ou Jogador vs IA
    if mode in [1, 2]:
        try:
            while True:
                try:
                    print("\nQuem começa? (1: X, 2: O)")
                    first_player = safe_int_input("Escolha: ")
                    while first_player not in [1, 2]:  # Garante escolha válida
                        print("Escolha inválida.")
                        first_player = safe_int_input("Escolha (1: X, 2: O): ")
                except EOFError:
                    print("\nEntrada finalizada. Programa encerrado.")
                    break

                state = ConnectState()  # Novo estado para novo jogo
                if first_player == 2:
                    state.to_play = 2  # Define jogador O a começar

                if mode == 1:
                    # Jogador vs Jogador
                    while not state.game_over():
                        print("Estado atual do jogo:")
                        state.print()
                        print(f"Jogador {'1 (X)' if state.to_play == 1 else '2 (O)'}:")
                        try:
                            move = safe_input_with_restart_or_quit(
                                "Escolha uma coluna (0-6), 'restart' para reiniciar o jogo ou 'quit' para encerrar o jogo: "
                            )
                            if move.lower() == 'restart':
                                raise RestartGameException
                            elif move.lower() == 'quit':
                                raise QuitGameException
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
                                move = safe_input_with_restart_or_quit(
                                    "Escolha uma coluna (0-6), 'restart' para reiniciar ou 'quit' para sair: "
                                )
                                if move.lower() == 'restart':
                                    raise RestartGameException
                                elif move.lower() == 'quit':
                                    raise QuitGameException
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
                    # Jogador vs Computador
                    mcts = MCTS(state)
                    if first_player == 2:
                        print("Computador começa...")
                        mcts.search(8)  # Computador pensa
                        move = mcts.best_move()
                        print(f"MCTS (X) escolheu: {move}")
                        state.move(move)
                        mcts.move(move)
                        state.print()

                    while not state.game_over():
                        print("Estado atual do jogo:")
                        state.print()

                        try:
                            user_move = safe_input_with_restart_or_quit(
                                "Escolha uma coluna (0-6), 'restart' ou 'quit': "
                            )
                            if user_move.lower() == 'restart':
                                raise RestartGameException
                            elif user_move.lower() == 'quit':
                                raise QuitGameException
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
                                user_move = safe_input_with_restart_or_quit(
                                    "Escolha uma coluna (0-6), 'restart' ou 'quit': "
                                )
                                if user_move.lower() == 'restart':
                                    raise RestartGameException
                                elif user_move.lower() == 'quit':
                                    raise QuitGameException
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
        # Computador vs Computador
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
