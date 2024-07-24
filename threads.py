""" O objetivo desta atividade é desenvolver um programa que utilize threads para somar os elementos de um vetor. 
Você deve criar um programa que solicite ao usuário a quantidade de threads e o tamanho do vetor. 
Em seguida, gere um vetor com os valores preenchidos aleatoriamente. Divida o trabalho de soma dos elementos do vetor 
entre as threads. Por fim, meça o tempo de execução da solução sequencial (sem threads) e da solução paralela 
com diferentes quantidades de threads e tamanhos de vetor. Extra: Faça um gráfico do tempo 
de execuçāo x quantidade de threads para diferentes tamanhos de vetor.
"""

import random
import time
import threading
import matplotlib.pyplot as plt


num_threads = int(input("Digite a quantidade de threads: "))
vector_size = int(input("Digite o tamanho do vetor: "))

#gerando o vetor com numeros aleatorios.
vector = [random.randint(1, 100) for _ in range(vector_size)]

#funcao para somar o vetor.
def sequential_sum(vector):
    return sum(vector)


start_time = time.time()
seq_sum = sequential_sum(vector)
end_time = time.time()
sequential_time = end_time - start_time

print(f"Soma sequencial: {seq_sum}, Tempo: {sequential_time:.6f} segundos")

def partial_sum(start, end, vector, result, index):
    result[index] = sum(vector[start:end])

def parallel_sum(vector, num_threads):
    length = len(vector)
    chunk_size = length // num_threads
    threads = []
    results = [0] * num_threads

    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i != num_threads - 1 else length
        thread = threading.Thread(target=partial_sum, args=(start, end, vector, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum(results)

start_time = time.time()
par_sum = parallel_sum(vector, num_threads)
end_time = time.time()
parallel_time = end_time - start_time

print(f"Soma paralela: {par_sum}, Tempo: {parallel_time:.6f} segundos")

def measure_times(vector_sizes, thread_counts):
    results = {}

    for size in vector_sizes:
        vector = [random.randint(1, 100) for _ in range(size)]
        results[size] = {'sequential': 0, 'parallel': []}

        
        start_time = time.time()
        sequential_sum(vector)
        end_time = time.time()
        results[size]['sequential'] = end_time - start_time

        for num_threads in thread_counts:
            start_time = time.time()
            parallel_sum(vector, num_threads)
            end_time = time.time()
            results[size]['parallel'].append(end_time - start_time)

    return results

vector_sizes = [10000, 50000, 100000, 500000]
thread_counts = [1, 2, 4, 8, 16]
results = measure_times(vector_sizes, thread_counts)

def plot_results(results, thread_counts):
    plt.figure()
    
    for size, times in results.items():
        plt.plot(thread_counts, times['parallel'], label=f'Paralela (Vetor: {size})')
        plt.axhline(y=times['sequential'], linestyle='--', label=f'Sequencial (Vetor: {size})')

    plt.xlabel('Quantidade de Threads')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Tempo de Execução vs Quantidade de Threads para Diferentes Tamanhos de Vetor')
    plt.legend()
    plt.grid(True)
    plt.show()

plot_results(results, thread_counts)

