import turtle
import random

# Глобальные переменные
sc = None
turtles = []  # Теперь список черепах
win = False
winner_color = None  # Новый атрибут для хранения победителя

# Сохраняем t1 и t2 для обратной совместимости
t1 = None
t2 = None

def setup(turtle_specs=None):
    """
    Инициализирует гонку.
    turtle_specs — список кортежей (name, color). Если None — создаются 2 черепахи по умолчанию.
    """
    global sc, turtles, t1, t2, win, winner_color
    win = False
    winner_color = None

    if turtle_specs is None:
        # Старое поведение: 2 черепахи
        turtle_specs = [('Red', 'red'), ('Blue', 'blue')]

    sc = turtle.Screen()
    sc.setup(500, 500)

    turtles.clear()
    y_positions = [50 - i * 100 for i in range(len(turtle_specs))]  # Распределяем по Y

    for i, (name, color) in enumerate(turtle_specs):
        t = turtle.Turtle()
        t.color(color)
        t.shape('turtle')
        t.penup()
        t.goto(-150, y_positions[i])
        turtles.append((name, t))

    # Поддержка обратной совместимости
    if len(turtles) >= 1:
        t1 = turtles[0][1]
    if len(turtles) >= 2:
        t2 = turtles[1][1]
    # Если больше 2 — t1 и t2 всё равно указывают на первые две

def start_race():
    """Запускает гонку до первого победителя."""
    global win
    for _ in range(100):
        if not win:
            for name, t in turtles:
                t.forward(random.randint(1, 5))
            check_winner()
        else:
            break

def check_winner():
    """Проверяет, достигла ли какая-либо черепаха финиша (x > 150)."""
    global win, winner_color
    for name, t in turtles:
        if t.xcor() > 150:
            print(f"Winner is {name}!")
            win = True
            winner_color = name
            break  # Первый достигший — победитель

# Старый код запуска (для демонстрации) — можно закомментировать в production
# setup()
# start_race()
# sc.exitonclick()