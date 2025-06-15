import telebot
from telebot import types
import requests

TOKEN = ''
NEWS_API_KEY = ''
bot = telebot.TeleBot(TOKEN)

news_cache = []

def get_news(category=None, query=None):
    base_url = 'https://newsapi.org/v2/'

    if query:
        url = base_url + f'everything?q={query}&language=ru&apiKey={NEWS_API_KEY}'
    elif category:
        url = base_url + f'top-headlines?country=ru&category={category}&apiKey={NEWS_API_KEY}'
    else:
        url = base_url + f'top-headlines?country=ru&apiKey={NEWS_API_KEY}'

    response = requests.get(url)
    data = response.json()

    if data.get('status') == 'ok':
        return data.get('articles', [])
    else:
        return []


def generate_category_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = [
        types.KeyboardButton("Общие"),
        types.KeyboardButton("Бизнес"),
        types.KeyboardButton("Развлечения"),
        types.KeyboardButton("Здоровье"),
        types.KeyboardButton("Наука"),
        types.KeyboardButton("Спорт"),
        types.KeyboardButton("Технологии")
    ]

    markup.add(*buttons)
    return markup

def send_news_card(chat_id, article):
    title = article.get('title', 'Без заголовка')
    description = article.get('description', 'Нет описания')
    url = article.get('url')
    url_to_image = article.get('urlToImage')

    inline_markup = types.InlineKeyboardMarkup()
    if url:
        inline_btn = types.InlineKeyboardButton(text="Далее", url=url)
        inline_markup.add(inline_btn)

    if url_to_image:
        bot.send_photo(chat_id, url_to_image, caption=f"*{title}*\n\n{description}", parse_mode="Markdown", reply_markup=inline_markup)
    else:
        bot.send_message(chat_id, f"*{title}*\n\n{description}", parse_mode="Markdown", reply_markup=inline_markup)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в новостной бот!\nВыберите категорию или используйте команды.", reply_markup=generate_category_buttons())

@bot.message_handler(commands=['refresh'])
def refresh(message):
    global news_cache
    news_cache = get_news()
    if news_cache:
        bot.send_message(message.chat.id, "Новости обновлены!")
        for article in news_cache[:5]: 
            send_news_card(message.chat.id, article)
    else:
        bot.send_message(message.chat.id, "Не удалось обновить новости.")

@bot.message_handler(commands=['clean'])
def clean(message):
    global news_cache
    news_cache.clear()
    bot.send_message(message.chat.id, "Новостная лента очищена.")

@bot.message_handler(commands=['search'])
def search(message):
    msg = bot.send_message(message.chat.id, "Введите ключевые слова для поиска новостей:")
    bot.register_next_step_handler(msg, search_news)

def search_news(message):
    query = message.text
    results = get_news(query=query)
    if results:
        for article in results[:5]:
            send_news_card(message.chat.id, article)
    else:
        bot.send_message(message.chat.id, "По вашему запросу новости не найдены.")

@bot.message_handler(content_types=['text'])
def category_handler(message):
    query_map = {
        "Общие": "новости",
        "Бизнес": "бизнес",
        "Развлечения": "развлечения",
        "Здоровье": "здоровье",
        "Наука": "наука",
        "Спорт": "спорт",
        "Технологии": "технологии"
    }

    query = query_map.get(message.text)
    if query:
        articles = get_news(query=query)
        if articles:
            bot.send_message(message.chat.id, f"Новости по теме: {message.text}")
            for article in articles[:5]:
                send_news_card(message.chat.id, article)
        else:
            bot.send_message(message.chat.id, "Нет новостей по выбранной теме.")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите категорию с кнопок ниже.")


bot.polling(none_stop=True)
