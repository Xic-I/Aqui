import os
import psutil
import multiprocessing
import time
import threading

def carga_cpu():
    while True:
        pass

def aumentar_consumo_cpu():
    try:
        # Solicita ao usuário a intensidade da carga da CPU
        intensidade_cpu = 1
        if intensidade_cpu <= 0 or intensidade_cpu > 1:
            print("Intensidade inválida. Deve estar entre 0 e 1.")
            return

        # Calcula o número de processos para atingir a intensidade desejada
        num_processos_cpu = multiprocessing.cpu_count()
        processos_cpu = []

        for _ in range(num_processos_cpu):
            processo = multiprocessing.Process(target=carga_cpu)
            processo.start()
            processos_cpu.append(processo)

        while True:
            for processo in processos_cpu:
                processo.terminate()
                processo = multiprocessing.Process(target=carga_cpu)
                processo.start()
                processos_cpu.append(processo)
            time.sleep(intensidade_cpu)  # Controla a intensidade da carga da CPU

    except KeyboardInterrupt:
        print("Teste de CPU interrompido.")

def aumentar_consumo_memoria():
    try:
        consumo_memoria = 900  # Começa com 900 MB
        aumento = 900  # Aumenta em 900 MB a cada iteração
        limite_atingido = False  # Variável para verificar se o limite foi atingido

        vezes = 100

        for _ in range(vezes):
            if not limite_atingido:
                # Aumenta o consumo de memória
                processo = psutil.Process(os.getpid())
                consumo_atual = processo.memory_info().rss / (1024 * 1024)  # Em MB

                # Verifica se o consumo total ultrapassa o limite do sistema
                limite_sistema = psutil.virtual_memory().total / (1024 * 1024)  # Total de memória do sistema em MB
                if consumo_atual + consumo_memoria > limite_sistema:
                    print(f"Consumo de memória atingiu o limite do sistema ({limite_sistema:.2f} MB). Entrando em loop.")
                    limite_atingido = True
                    while True:
                        pass  # Loop infinito para manter o programa ativo
                else:
                    # Alocar memória adicional
                    novo_consumo = consumo_atual + consumo_memoria
                    memoria_adicional = bytearray(b'x' * int((consumo_memoria * 1024 * 1024)))

                    # Imprime informações sobre o consumo de memória
                    print(f"Consumo de memória atual: {consumo_atual:.2f} MB")
                    print(f"Consumo de memória após alocação: {novo_consumo:.2f} MB")
                    print(f"Alocação de memória: {consumo_memoria} MB")

                    # Atualiza o valor de consumo_memoria para a próxima iteração
                    consumo_memoria += aumento

    except KeyboardInterrupt:
        print("Teste de memória interrompido.")

if __name__ == "__main__":
    thread_cpu = threading.Thread(target=aumentar_consumo_cpu)
    thread_memoria = threading.Thread(target=aumentar_consumo_memoria)

    thread_cpu.start()
    thread_memoria.start()

    thread_cpu.join()
    thread_memoria.join()
