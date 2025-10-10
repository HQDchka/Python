import multiprocessing
import time


def worker(task_queue):
    """
    Рабочий процесс, который получает задания из очереди.
    Если задание == 'STOP', процесс завершает работу.
    """
    process_name = multiprocessing.current_process().name
    while True:
        task = task_queue.get()  # получаем задание из очереди
        if task == 'STOP':       # сигнал завершения работы
            print(f"[{process_name}] завершает работу.")
            break
        # имитация обработки задания
        print(f"[{process_name}] обработал задание: {task}")
        time.sleep(0.5)  # чтобы было видно порядок выполнения


if __name__ == '__main__':
    tasks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    num_workers = 3

    # Создаём очередь для обмена данными между процессами
    task_queue = multiprocessing.Queue()

    # Создаём и запускаем 3 рабочих процесса
    processes = []
    for i in range(num_workers):
        p = multiprocessing.Process(target=worker, args=(task_queue,), name=f"Worker-{i+1}")
        processes.append(p)
        p.start()

    # Добавляем задания в очередь
    for task in tasks:
        task_queue.put(task)

    # Добавляем сигналы остановки (по одному для каждого процесса)
    for _ in range(num_workers):
        task_queue.put('STOP')

    # Дожидаемся завершения всех процессов
    for p in processes:
        p.join()

    print("Все задания выполнены!")


"""
Потому что у нас запущено 3 независимых рабочих процесса.
Каждый процесс ждёт задание из очереди и блокируется на операции .get().
Если бы мы положили только один 'STOP', его получил бы только один процесс —
остальные продолжали бы ждать задание бесконечно и никогда не завершились бы.

Поэтому мы помещаем по одному сигналу 'STOP' на каждый процесс,
чтобы каждый из них получил свой собственный сигнал завершения.
"""
