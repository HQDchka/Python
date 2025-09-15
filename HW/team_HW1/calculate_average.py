def calculate_average(numbers):
    """
    Вычисляет среднее значение списка чисел.
    Возвращает None, если список пуст.
    """
    if not numbers:
        return None

    return sum(numbers) / len(numbers)  


# Пример использования
numbers_list = [10, 20, 30, 40]
result = calculate_average(numbers_list)
if result is not None:
    print(f"Среднее значение: {result}")
else:
    print("Список пуст")
