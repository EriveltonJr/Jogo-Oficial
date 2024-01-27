import threading
import time
import random

# Definindo um semáforo para controlar o acesso à variável compartilhada (resultado e pontuação)
semaphore = threading.Semaphore(1)

# Variáveis compartilhadas
resultado = None
pontuacao_jogadores = {i: 0 for i in range(1, 6)}  # Inicializa a pontuação de cada jogador

# Função que calcula a tabuada, permite que os jogadores e o usuário dêem seus palpites e atualiza o resultado e a pontuação
def calcular_tabuada(identificador, numero_tabuada):
    global resultado

    for i in range(1, 11):  # Calcular a tabuada de 1 a 10
        # Aguarda um momento aleatório antes de calcular
        time.sleep(random.uniform(0.1, 0.5))

        # Adquire o semáforo (bloqueia se necessário)
        semaphore.acquire()
        try:
            # Jogadores dão seus palpites
            palpites_jogadores = {jogador: random.randint(1, 100) for jogador in pontuacao_jogadores.keys()}

            # Usuário dá seu palpite
            while True:
                try:
                    palpite_usuario = int(input("\nDigite seu palpite (entre 1 e 100): "))
                    if 1 <= palpite_usuario <= 100:
                        break
                    else:
                        print("Palpite inválido. Digite um número entre 1 e 100.")
                except ValueError:
                    print("Entrada inválida. Digite um número inteiro.")

            print(f"\nThread {identificador} está calculando {numero_tabuada} x {i}.")
            print(f"Palpites dos jogadores: {palpites_jogadores}")
            print(f"Palpite do usuário: {palpite_usuario}")

            # Calcula e atualiza o resultado
            resultado = numero_tabuada * i
            print(f"Thread {identificador} calculou {numero_tabuada} x {i} = {resultado}.")

            # Avalia os palpites e atualiza a pontuação
            for jogador, palpite in palpites_jogadores.items():
                if palpite == resultado:
                    print(f"Jogador {jogador} acertou o palpite ({palpite}) e ganhou 10 pontos!")
                    pontuacao_jogadores[jogador] += 10

            # Avalia o palpite do usuário e atualiza a pontuação
            if palpite_usuario == resultado:
                print("Você acertou o palpite e ganhou 10 pontos!")
                pontuacao_jogadores["Usuario"] = 10

        finally:
            # Libera o semáforo, permitindo que outras threads realizem o cálculo e dêem seus palpites
            semaphore.release()

# 5 threads para calcular diferentes tabuadas simultaneamente
threads = []
for i in range(5):
    numero_tabuada = random.randint(1, 10)  # Cada thread escolhe uma tabuada aleatória
    thread = threading.Thread(target=calcular_tabuada, args=(i+1, numero_tabuada))
    threads.append(thread)
    thread.start()

# Aguarda todas as threads terminarem antes de exibir o resultado final e a pontuação
for thread in threads:
    thread.join()

print("\nPontuação final dos jogadores:")
for jogador, pontuacao in pontuacao_jogadores.items():
    print(f"{jogador}: {pontuacao} pontos")