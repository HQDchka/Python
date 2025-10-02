import turtle
import random
from sprint import setup, start_race, turtles, win, winner_color

class TurtleRaceAPI:
    """Современная обертка для управления унаследованными черепашьими бегами."""

    def __init__(self):
        self.turtle_specs = []  # Список (name, color)
        self.is_race_finished = False
        self.winner = None
        # Изначально добавляем две черепахи для совместимости
        self.add_turtle('Red', 'red')
        self.add_turtle('Blue', 'blue')
        self._apply_setup()

    def add_turtle(self, name, color):
        """Добавляет новую черепаху в гонку. Требуется перезапуск setup."""
        self.turtle_specs.append((name, color))

    def _apply_setup(self):
        """Применяет текущий список черепах к legacy-коду."""
        setup(self.turtle_specs)
        self.is_race_finished = False
        self.winner = None

    def start_race(self):
        """Запускает гонку и возвращает победителя."""
        start_race()

        self.is_race_finished = win
        self.winner = winner_color if winner_color else 'Draw'
        return self.winner

    def get_winner(self):
        return self.winner

    def get_turtle_positions(self):
        """Возвращает позиции всех черепах."""
        return {name: (t.xcor(), t.ycor()) for name, t in turtles}

    def reset_race(self):
        """Сбрасывает и пересоздаёт гонку с текущим набором черепах."""
        self._apply_setup()


# Пример использования
race_manager = TurtleRaceAPI()

# Добавим третью черепаху
race_manager.add_turtle('Green', 'green')

print("Запускаем гонку №1!")
winner = race_manager.start_race()
print(f"Победитель: {winner}")
print(f"Позиции: {race_manager.get_turtle_positions()}")

answer = input("Запустить еще одну гонку? (y/n): ")
if answer.lower() == 'y':
    race_manager.reset_race()
    print("\nЗапускаем гонку №2!")
    winner = race_manager.start_race()
    print(f"Победитель: {winner}")

turtle.Screen().exitonclick()