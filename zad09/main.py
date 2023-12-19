import math
import threading
import os


def prime(num):
    if num < 2:
        return False
    sqrt_k = math.isqrt(num)
    for i in range(2, sqrt_k + 1):
        if num % i == 0:
            return False
    return True


def find_primes(start, end, result, barrier):
    primes = []
    print(f"{threading.current_thread().name} liczy w przedziale od {start} do {end}")
    for i in range(start, end + 1):
        if prime(i):
            primes.append(i)

    print(f"{threading.current_thread().name} znalazł: {primes}")
    result.extend(primes)
    barrier.wait()


def main():
    available_threads = os.cpu_count()
    start = int(input("Podaj początek przedziału: "))
    end = int(input("Podaj koniec przedziału: "))
    print("Maksymalna liczba wątków -", available_threads)
    threads_count = int(input("Podaj liczbę wątków: "))

    if start >= end:
        print("Początek przedziału musi być mniejszy od końca przedziału")
        return

    if threads_count < 1:
        print("Liczba wątków musi być większa od 0")
        return
    elif threads_count > available_threads:
        print("Podano więcej wątków niż posiada komputer")
        return

    chunk_size = (end - start + 1) // threads_count
    threads = []
    primes = []
    barrier = threading.Barrier(threads_count + 1)

    for i in range(threads_count):
        start_range = start + i * chunk_size

        if i != threads_count - 1:
            end_range = start_range + chunk_size - 1
        else:
            end_range = end

        thread = threading.Thread(target=find_primes, args=(start_range, end_range, primes, barrier), name=f"Wątek-{i+1}")
        threads.append(thread)
        thread.start()

    barrier.wait()
    print("Liczby pierwsze:", primes)


if __name__ == "__main__":
    main()
