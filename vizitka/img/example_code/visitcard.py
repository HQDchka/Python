import tkinter as tk
from tkinter import ttk, font
import webbrowser

class BusinessCardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Моя визитка")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Загрузка шрифтов (используем системные)
        self.bold_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=10)
        self.small_font = font.Font(family="Helvetica", size=8)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Основной фрейм с тенью
        main_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RAISED)
        main_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        
        # Верхняя часть с фото и именем
        top_frame = tk.Frame(main_frame, bg="#2c3e50")
        top_frame.pack(fill=tk.X)
        
        # Фото (заглушка)
        photo_placeholder = tk.Label(top_frame, bg="#2c3e50", fg="white", 
                                    text="ФОТО", font=self.title_font)
        photo_placeholder.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Имя и должность
        name_frame = tk.Frame(top_frame, bg="#2c3e50")
        name_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=20)
        
        tk.Label(name_frame, text="Иван Иванов", bg="#2c3e50", fg="white", 
                font=self.title_font).pack(anchor=tk.W)
        tk.Label(name_frame, text="Старший разработчик Python", bg="#2c3e50", 
                fg="#ecf0f1", font=self.normal_font).pack(anchor=tk.W)
        
        # Разделитель
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # Контактная информация
        contact_frame = tk.Frame(main_frame, bg="#ffffff")
        contact_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.create_contact_entry(contact_frame, "Телефон:", "+7 (123) 456-78-90")
        self.create_contact_entry(contact_frame, "Email:", "ivanov@example.com")
        self.create_contact_entry(contact_frame, "Сайт:", "example.com", is_link=True)
        self.create_contact_entry(contact_frame, "GitHub:", "github.com/ivanov", is_link=True)
        
        # Разделитель
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # О себе
        about_frame = tk.Frame(main_frame, bg="#ffffff")
        about_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(about_frame, text="О себе:", bg="#ffffff", 
                font=self.bold_font).pack(anchor=tk.W)
        
        about_text = ("Опытный Python-разработчик с более чем 5-летним стажем. "
                     "Специализация: веб-приложения, анализ данных и автоматизация. "
                     "Увлекаюсь созданием чистого и эффективного кода.")
        
        about_label = tk.Label(about_frame, text=about_text, bg="#ffffff", 
                              font=self.normal_font, wraplength=400, justify=tk.LEFT)
        about_label.pack(anchor=tk.W)
        
        # Кнопки действий
        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(button_frame, text="Связаться", bg="#3498db", fg="white",
                font=self.normal_font, relief=tk.FLAT,
                command=self.contact_me).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Проекты", bg="#2ecc71", fg="white",
                font=self.normal_font, relief=tk.FLAT,
                command=self.show_projects).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Закрыть", bg="#e74c3c", fg="white",
                font=self.normal_font, relief=tk.FLAT,
                command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
        # Статус бар
        status_bar = tk.Label(main_frame, text="Готово", bg="#ecf0f1", 
                             font=self.small_font, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)
    
    def create_contact_entry(self, parent, label, value, is_link=False):
        frame = tk.Frame(parent, bg="#ffffff")
        frame.pack(fill=tk.X, pady=2)
        
        tk.Label(frame, text=label, bg="#ffffff", font=self.bold_font, 
                width=10, anchor=tk.W).pack(side=tk.LEFT)
        
        if is_link:
            link = tk.Label(frame, text=value, bg="#ffffff", fg="#3498db", 
                           font=self.normal_font, cursor="hand2")
            link.pack(side=tk.LEFT, fill=tk.X)
            link.bind("<Button-1>", lambda e: self.open_link(value))
        else:
            tk.Label(frame, text=value, bg="#ffffff", font=self.normal_font).pack(side=tk.LEFT)
    
    def open_link(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        webbrowser.open_new(url)
    
    def contact_me(self):
        # В реальном приложении здесь могла бы быть форма обратной связи
        print("Форма связи открыта")
    
    def show_projects(self):
        # В реальном приложении здесь мог бы быть список проектов
        print("Список проектов открыт")

if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessCardApp(root)
    root.mainloop()