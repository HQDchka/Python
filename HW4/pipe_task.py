import multiprocessing
import time


def ping_pong(conn, message, max_count):
    """
    Функция, реализующая обмен сообщениями через канал.
    Процесс получает сообщение, печатает его и отправляет своё в ответ.
    """
    count = 0
    process_name = multiprocessing.current_process().name

    while count < max_count:
        msg = conn.recv()  # получить сообщение из канала
        print(f"[{process_name}] получил: {msg}")

        time.sleep(0.5)  # задержка для наглядности

        conn.send(message)  # отправить своё сообщение обратно
        count += 1


if __name__ == '__main__':
    # Создаём двусторонний канал
    parent_conn, child_conn = multiprocessing.Pipe()

    max_messages = 5

    # Создаём дочерний процесс
    p = multiprocessing.Process(
        target=ping_pong,
        args=(child_conn, 'Понг!', max_messages),
        name="Child"
    )
    p.start()

    # Главный процесс (родитель)
    print("[Parent] запускает игру.")
    parent_conn.send("Старт!")  # отправляем первое сообщение

    # Родитель тоже участвует в "пинг-понге"
    ping_pong(parent_conn, 'Пинг!', max_messages)

    # Ожидаем завершения дочернего процесса
    p.join()

    print("Игра окончена!")


"""
Метод join() заставляет главный процесс дождаться завершения дочернего.
Если убрать p.join(), главный процесс может завершиться раньше,
чем дочерний закончит обмен сообщениями.

В результате программа может:
- завершиться преждевременно;
- вывести неполные данные;
- а на некоторых системах — прервать дочерний процесс принудительно.

Поэтому p.join() обязательно нужен, чтобы синхронизировать завершение
и корректно дождаться конца работы дочернего процесса.
"""
