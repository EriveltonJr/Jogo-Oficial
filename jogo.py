import threading
import time
import random

# Definindo um semáforo para controlar o acesso à variável compartilhada (resultado e pontuação)
semaphore = threading.Semaphore(1)

# Variáveis compartilhadas
resultado = None
pontuacao_jogadores = {i: 0 for i in range(1, 6)}  # Inicializa a pontuação de cada jogador
numero_tabuada = 9  

# Função que calcula a tabuada, permite que os jogadores adivinhem e atualiza o resultado e a pontuação
def calcular_tabuada(identificador):
    global resultado

    for i in range(1, 11):  # Calcula a tabuada de 1 a 10
        
        time.sleep(random.uniform(0.1, 0.5))

        print(f"\nThread {identificador} está calculando {numero_tabuada} x {i}.")
        # Adquire o semáforo (bloqueia se necessário)
        semaphore.acquire()
        try:
            # Calcula e atualiza o resultado
            resultado = numero_tabuada * i
            print(f"Thread {identificador} calculou {numero_tabuada} x {i} = {resultado}.")

            for jogador, pontuacao in pontuacao_jogadores.items():
                palpite = random.randint(1, 100)
                if palpite == resultado:
                    print(f"Jogador {jogador} acertou o palpite ({palpite}) e ganhou 10 pontos!")
                    pontuacao_jogadores[jogador] += 10
        finally:
            # Libera o semáforo, permitindo que outras threads realizem o cálculo e adivinhem
            semaphore.release()

# 5 threads para calcular a tabuada simultaneamente
threads = []
for i in range(5):
    thread = threading.Thread(target=calcular_tabuada, args=(i+1,))
    threads.append(thread)
    thread.start()

# Aguarda todas as threads terminarem antes de exibir o resultado final e a pontuação
for thread in threads:
    thread.join()

print(f"\nTabuada completa de {numero_tabuada}:")
for i in range(1, 11):
    print(f"{numero_tabuada} x {i} = {numero_tabuada * i}")

print("\nPontuação final dos jogadores:")
for jogador, pontuacao in pontuacao_jogadores.items():
    print(f"Jogador {jogador}: {pontuacao} pontos")