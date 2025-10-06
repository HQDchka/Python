import time
import threading
from multiprocessing import Pool

# Функция для вычисления факториала числа
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# Последовательное выполнение
def run_sequential(numbers):
    start_time = time.time()
    results = []
    for num in numbers:
        results.append(factorial(num))
    end_time = time.time()
    print(f"Последовательное выполнение заняло: {end_time - start_time:.2f} секунд")

# Многопоточное выполнение
def run_threads(numbers):
    threads = []
    start_time = time.time()
    for num in numbers:
        thread = threading.Thread(target=factorial, args=(num,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Многопоточное выполнение заняло: {end_time - start_time:.2f} секунд")

# Многопроцессное выполнение
def run_processes(numbers):
    pool = Pool(processes=len(numbers))
    start_time = time.time()
    pool.map(factorial, numbers)
    end_time = time.time()
    pool.close()
    pool.join()
    print(f"Выполнение с процессами заняло: {end_time - start_time:.2f} секунд")

if __name__ == "__main__":
    numbers = [100000, 100000]
    run_sequential(numbers)
    run_threads(numbers)
    run_processes(numbers)


"""
1. При последовательном выполнении — все вычисления выполняются по очереди в одном потоке.
   Это самый медленный вариант, так как используется только одно ядро процессора.

2. При многопоточном выполнении — программа всё ещё ограничена GIL (Global Interpreter Lock),
   из-за чего в каждый момент времени реально работает только один поток Python.
   Потоки переключаются, но не выполняются одновременно — ускорения почти нет.

3. При многопроцессном выполнении — каждый процесс имеет собственный интерпретатор Python
   и свой GIL, поэтому процессы выполняются параллельно на разных ядрах CPU.
   Это позволяет действительно использовать все ядра и значительно ускоряет выполнение.
"""
# Вывод:
# Последовательное выполнение заняло: 6.60 секунд
# Многопоточное выполнение заняло: 5.49 секунд
# Выполнение с процессами заняло: 3.30 секунд