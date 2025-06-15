import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

''' Основная функция приложения '''
def create_visiting_card():
    # Базовые настройки окна
    app = tk.Tk()
    app.title('Моя визитная карточка')
    app.geometry('800x600')
    app.resizable(False, False)
    # app.iconbitmap()

    # Формирование основных стилей
    style = ttk.Style()
    style.configure('TFrame', background = '#01161E')
    style.configure('TLabel', background = '#A4692B', font=('Arial',12))
    style.configure('Header.TLabel', font=('Arial', 18, 'bold'))

    main_frame = ttk.Frame(app)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Заголовок
    header = ttk.Label(main_frame, text='Моя визитная карточка', style='Header.TLabel')
    header.pack(pady=20)

    # Фото (заглушка)
    image = PhotoImage(file="vizitka/img/cat.png")
    photo_label = ttk.Label(main_frame, image=image)
    photo_label.pack()

    # Информация
    info_frame = ttk.Frame(main_frame)
    info_frame.pack(pady=20)

    ttk.Label(info_frame, text='Имя: Иван Иванов').grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
    ttk.Label(info_frame, text='Профессия: Python-разработчик').grid(row=1, column=0, sticky=tk.W, padx=10, pady=7)
    ttk.Label(info_frame, text='eMail: info@ittop-colledge.ru').grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    ttk.Label(info_frame, text='Телефон: +7 (123) 456-78-90').grid(row=3, column=0, sticky=tk.W, padx=10, pady=7)

    # Кнопки
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=20)

    ttk.Button(button_frame, text='Портфолио', command=lambda: show_portfolio()).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text='Контакты', command=lambda: show_contacts()).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text='Выход', command=app.quit).pack(side=tk.LEFT, padx=10)

    # Сборка приложения
    app.mainloop()

def show_portfolio():
    portfolio_window = tk.Toplevel()
    portfolio_window.title('Портфолио')
    ttk.Label(portfolio_window, text='[Здесь будет портфолио]').pack(padx=50, pady=50)

def show_contacts():
    contacts_window = tk.Toplevel()
    contacts_window.title('Контакты')
    ttk.Label(contacts_window, text='[Здесь будут дополнительные контакты]').pack(padx=50, pady=50)

''' Запуск приложения (вызов основной функции)'''
create_visiting_card()