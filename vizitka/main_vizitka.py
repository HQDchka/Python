import sys
import webbrowser
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt


# Окно с контактной информацией
class ContactsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Контакты")

        layout = QVBoxLayout()

        # Кнопки, копирующие email и телефон в буфер обмена
        btn_email = QPushButton("Email: daniilgaponov05@gmail.com")
        btn_phone = QPushButton("Телефон: +7 995 447-20-07")

        # При нажатии копируется соответствующий текст
        btn_email.clicked.connect(lambda: QApplication.clipboard().setText("daniilgaponov05@gmail.com"))
        btn_phone.clicked.connect(lambda: QApplication.clipboard().setText("+7 995 447-20-07"))

        layout.addWidget(btn_email)
        layout.addWidget(btn_phone)

        # Кнопки для открытия профилей в Telegram и ВКонтакте
        btn_telegram = QPushButton("Telegram")
        btn_vk = QPushButton("VK")
        btn_telegram.clicked.connect(lambda: webbrowser.open("https://t.me/HQD_Daniil"))
        btn_vk.clicked.connect(lambda: webbrowser.open("https://vk.com/dgaponov5"))

        # Горизонтальное размещение кнопок соцсетей
        social_layout = QHBoxLayout()
        social_layout.addWidget(btn_telegram)
        social_layout.addWidget(btn_vk)

        layout.addLayout(social_layout)
        self.setLayout(layout)
        self.setFixedSize(300, 170)


# Окно с портфолио проектов
class PortfolioWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Портфолио")
        layout = QVBoxLayout()

        # Словарь с проектами и их GitHub-ссылками
        projects = {
            "Работы с Kotlin и Java": "https://github.com/HQDchka/mobile_development",
            "Telegram-боты": "https://github.com/HQDchka/Python/tree/main/Telegram_bots",
            "База данных сайта учебного учреждения": "https://github.com/HQDchka/SQL_Journal"
        }

        # Добавляем каждый проект как кликабельную HTML-ссылку
        for name, url in projects.items():
            link = QLabel(f'<a href="{url}" style="color: #00ccff;">✅ {name}</a>')
            link.setOpenExternalLinks(True)
            link.setTextInteractionFlags(Qt.TextBrowserInteraction)
            link.setCursor(Qt.PointingHandCursor)
            layout.addWidget(link)

        # Кнопка с ссылкой на профиль GitHub
        btn_github = QPushButton("GitHub: HQDchka")
        btn_github.clicked.connect(lambda: webbrowser.open("https://github.com/HQDchka"))
        layout.addWidget(btn_github)

        self.setLayout(layout)
        self.setFixedSize(350, 180)


# Окно с фотогалереей
class GalleryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Фотогалерея")

        scroll = QScrollArea()         # Область прокрутки
        widget = QWidget()             # Внутренний контейнер
        layout = QGridLayout()         # Сетка для изображений

        # Список путей к изображениям
        image_files = [
            "vizitka/img/kotlin.jpg",
            "vizitka/img/Csharp.jpg",
            "vizitka/img/phpmyadmin.png",
            "vizitka/img/GitHub.png"
        ]

        # Загружаем каждое изображение и добавляем в сетку
        for i, img_path in enumerate(image_files):
            pic = QLabel()
            pixmap = QPixmap(img_path).scaled(
                900, 900, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            pic.setPixmap(pixmap)
            layout.addWidget(pic, i, 0)

        widget.setLayout(layout)
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        self.setFixedSize(900, 600)


# Главное окно визитки
class BusinessCardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Визитная карточка")
        self.setMinimumSize(500, 400)
        self.init_ui()

    # Метод инициализации интерфейса
    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(20)

        # Верхний блок с фотографией и текстом
        info_layout = QHBoxLayout()

        photo = QLabel()
        pixmap = QPixmap("vizitka/img/avatarka.jpg").scaled(
            200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        photo.setPixmap(pixmap)
        photo.setAlignment(Qt.AlignTop)

        # Блок с текстом: имя и описание
        text_layout = QVBoxLayout()
        name = QLabel("Гапонов Даниил")
        name.setFont(QFont("Arial", 20, QFont.Bold))
        name.setAlignment(Qt.AlignLeft)

        about = QLabel(
            "Студент колледжа, специализация: Разработка Программного обеспечения.\n"
            "Изучаю Python, C++, C#, Kotlin."
        )
        about.setWordWrap(True)
        about.setAlignment(Qt.AlignLeft)

        text_layout.addWidget(name)
        text_layout.addWidget(about)

        info_layout.addWidget(photo)
        info_layout.addLayout(text_layout)
        self.main_layout.addLayout(info_layout)

        # Создание окон, которые будут открываться по кнопкам
        self.contacts_window = ContactsWindow()
        self.portfolio_window = PortfolioWindow()
        self.gallery_window = GalleryWindow()

        # Кнопки открытия других окон
        btn_contacts = QPushButton("📞 Контакты")
        btn_contacts.clicked.connect(self.contacts_window.show)

        btn_portfolio = QPushButton("📁 Портфолио")
        btn_portfolio.clicked.connect(self.portfolio_window.show)

        btn_gallery = QPushButton("🖼️ Фотогалерея")
        btn_gallery.clicked.connect(self.gallery_window.show)

        # Добавляем кнопки в главный интерфейс
        for btn in (btn_contacts, btn_portfolio, btn_gallery):
            btn.setFixedHeight(35)
            self.main_layout.addWidget(btn)

        self.setLayout(self.main_layout)


# Точка входа в программу
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Общий стиль для всего интерфейса
    app.setStyleSheet("""
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            font-size: 14px;
        }
        QPushButton {
            background-color: #444;
            color: white;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #666;
        }
        QScrollArea {
            border: none;
        }
        QLabel {
            font-size: 14px;
        }
    """)

    window = BusinessCardApp()
    window.show()
    sys.exit(app.exec())
