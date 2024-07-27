import threading
import random
import time


def ponts(num_samples, result, index):
    count = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1:
            count += 1
    result[index] = count


def calculate_pi(num_samples, num_threads):
    samples_per_thread = num_samples // num_threads
    threads = []
    results = [0] * num_threads

    for i in range(num_threads):
        thread = threading.Thread(target=ponts, args=(samples_per_thread, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_count = sum(results)
    pi_estimate = (total_count / num_samples) * 4
    return pi_estimate


num_samples = int(input("Digite o número de amostras: "))
num_threads = int(input("Digite o número de threads: "))


start_time = time.time()
pi_estimate = calculate_pi(num_samples, num_threads)
end_time = time.time()

execution_time = end_time - start_time

print(f"Estimativa de pi: {pi_estimate}")
print(f"Tempo de execução: {execution_time:.6f} segundos")

