def calculate_average(numbers):
    """
    Функция вычисляет среднее арифметическое списка чисел.
    
    :param numbers: список чисел (int или float)
    :return: среднее значение или None, если список пуст
    """
    if not numbers:
        return None
    
    return sum(numbers) / len(numbers)


def main():
    numbers_list = [10, 20, 30, 40]
    result = calculate_average(numbers_list)
    
    if result is not None:
        print(f"Среднее значение: {result:.2f}")
    else:
        print("Список пуст")


if __name__ == "__main__":
    main()

'''
Что было сделано

Упрощена проверка на пустой список

Вместо if len(numbers) == 0: → if not numbers

Удалены лишние переменные

Необязательно хранить total и average — результат можно вернуть сразу:

Добавлена документация (docstring)

Вынесен код в функцию main()

Форматирование вывода

Вывод среднего значения ограничен до двух знаков после запятой: {result:.2f}.

Использован шаблон if __name__ == "__main__":
'''