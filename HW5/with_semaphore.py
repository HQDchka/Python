import time
from multiprocessing import Process, Semaphore

def writer(filename, data, count, sem):
    """Функция-писатель, использующая семафор для синхронизации"""
    # Захватываем семафор перед началом записи
    sem.acquire()
    try:
        with open(filename, 'a') as f:
            for _ in range(count):
                time.sleep(0.01)  # Имитация долгой работы
                f.write(data)
                time.sleep(0.01)
    finally:
        # Освобождаем семафор даже если произойдет ошибка
        sem.release()

if __name__ == '__main__':
    filename = 'shared_file_sem.txt'
    data_a = 'A' * 50 + '\n'
    data_b = 'B' * 50 + '\n'

    # Создаем семафор (1 процесс может работать с файлом одновременно)
    sem = Semaphore(1)

    proc1 = Process(target=writer, args=(filename, data_a, 10, sem))
    proc2 = Process(target=writer, args=(filename, data_b, 10, sem))
    proc1.start()
    proc2.start()

    proc1.join()
    proc2.join()

    print("Запись завершена. Проверьте файл 'shared_file_sem.txt'.")

"""
Анализ результата:
Теперь содержимое файла всегда выглядит аккуратно и предсказуемо:

Пример результата:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
...
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB

Что изменилось:
Семафор (Semaphore(1)) обеспечивает, что только один процесс за раз
выполняет запись в файл. Второй процесс ждёт, пока первый не освободит семафор.

Как это решает проблему:
Теперь операция записи в файл (несколько вызовов write подряд)
происходит последовательно, без прерываний.
Нет состояния гонки — данные не перемешиваются.

Итог:
Race condition устранена.
Данные записываются поочередно и корректно.
"""
