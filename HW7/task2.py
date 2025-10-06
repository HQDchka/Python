from multiprocessing import Process, Value
import ctypes

def increment(shared_counter):
    for _ in range(1_000_000):
        with shared_counter.get_lock():  # защищаем общий ресурс
            shared_counter.value += 1

if __name__ == "__main__":
    # Глобальная переменная для тестирования (в разделяемой памяти)
    counter = Value(ctypes.c_int, 0)

    # Создаем процессы
    process1 = Process(target=increment, args=(counter,))
    process2 = Process(target=increment, args=(counter,))

    # Запускаем оба процесса одновременно
    process1.start()
    process2.start()

    # Ждем завершения обоих процессов
    process1.join()
    process2.join()

    print(f'Итоговое значение счётчика: {counter.value}')


"""
1. В модуле multiprocessing каждый процесс создаётся со своим собственным 
   интерпретатором Python и, соответственно, со своим собственным GIL.

2. Это позволяет выполнять вычисления действительно параллельно 
   (например, на разных ядрах процессора).

3. Для обмена данными между процессами используется объект Value, 
   который хранится в общей памяти. Блокировка get_lock() предотвращает 
   одновременную запись и обеспечивает корректный результат.

4. Итоговое значение счётчика также будет равно 2_000_000, но теперь 
   операции выполняются параллельно, а не последовательно.

5. Различие между threading и multiprocessing:
   - threading: GIL не даёт потокам работать одновременно → последовательное выполнение.
   - multiprocessing: каждый процесс независим → параллельное выполнение без GIL.
"""
