from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.core.window import Window

Window.size = (800, 600)

class VisitingCardApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Заголовок
        title = Label(text='Моя визитная карточка', font_size=24, bold=True)
        layout.add_widget(title)

        # Фото (заглушка)
        photo = Image(source='photos/kat.png', size_hint=(None, None), size=(200, 200))
        layout.add_widget(photo)

        # Информация
        info = Label(text='Имя: Иван Иванов\nПрофессия: Python-разработчик\neMail: info@ittop-colledge.ru\nТелефон: +7 (123) 456-78-90')
        layout.add_widget(info)

        # Кнопки
        button_layout = BoxLayout(spacing=10)

        portfolio_btn = Button(text='Портфолио')
        portfolio_btn.bind(on_press=self.show_portfolio)
        button_layout.add_widget(portfolio_btn)

        contacts_btn = Button(text='Контакты')
        contacts_btn.bind(on_press=self.show_contacts)
        button_layout.add_widget(contacts_btn)

        exit_btn = Button(text='Выход')
        exit_btn.bind(on_press=lambda x: App.get_running_app().stop())
        button_layout.add_widget(exit_btn)

        layout.add_widget(button_layout)

        return layout

    def show_portfolio(self, instance):
        content = Label(text='[Здесь будет портфолио]')
        popup = Popup(title='Портфолио', content=content, size_hint=(None, None), size=(400, 300))
        popup.open()

    def show_contacts(self, instance):
        content = Label(text='[Здесь будут дополнительные контакты]')
        popup = Popup(title='Контакты', content=content, size_hint=(None, None), size=(400, 300))
        popup.open()

VisitingCardApp().run()