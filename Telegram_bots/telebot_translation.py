import os
import telebot
from telebot import types
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS

# Токен бота
token = '6618115945:AAFRlyS3uHgzsAiBzpvOn7BJWCI8jEhinDs'
bot = telebot.TeleBot(token)

# Хранилище состояний
user_states = {}

# Список поддерживаемых языков
LANGUAGES = {
    '🇬🇧 Английский': 'en',
    '🇷🇺 Русский': 'ru',
    '🇪🇸 Испанский': 'es',
    '🇫🇷 Французский': 'fr',
    '🇩🇪 Немецкий': 'de',
    '🇮🇹 Итальянский': 'it',
    '🇵🇹 Португальский': 'pt',
    '🇨🇳 Китайский': 'zh-CN',
    '🇯🇵 Японский': 'ja',
    '🇰🇷 Корейский': 'ko',
    '🇦🇪 Арабский': 'ar',
    '🇮🇳 Хинди': 'hi'
}

# Обратный словарь для отображения языка на русском
LANG_CODES_TO_NAMES = {v: k.split()[1] for k, v in LANGUAGES.items()}

def language_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=lang, callback_data=code) for lang, code in LANGUAGES.items()]
    keyboard.add(*buttons)
    return keyboard

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('🔤 Перевести текст', 'ℹ️ О боте')
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        f"Привет, {message.from_user.first_name}! Я бот для перевода текста.",
        reply_markup=main_menu())

@bot.message_handler(func=lambda msg: msg.text == 'ℹ️ О боте')
def about(message):
    bot.send_message(message.chat.id, "🤖 Бот-переводчик с поддержкой TTS и оценкой перевода.")

@bot.message_handler(func=lambda msg: msg.text == '🔤 Перевести текст')
def translate_request(message):
    msg = bot.send_message(message.chat.id, "📝 Введите текст для перевода:")
    bot.register_next_step_handler(msg, handle_text_input)

def handle_text_input(message):
    text = message.text
    user_states[message.chat.id] = {'text': text}

    # Клавиатура для выбора исходного языка
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton("🔍 Автоопределение", callback_data="auto"))
    for lang, code in LANGUAGES.items():
        keyboard.add(types.InlineKeyboardButton(text=lang, callback_data=f"src_{code}"))
    bot.send_message(message.chat.id, "🌐 Выберите язык, с которого переводим:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    user_data = user_states.get(chat_id, {})

    # Выбор исходного языка
    if call.data.startswith("src_"):
        src_lang = call.data[4:]
        user_states[chat_id]['source_lang'] = src_lang
        ask_target_language(chat_id)

    # Автоопределение языка
    elif call.data == "auto":
        text = user_data.get('text')
        if not text:
            bot.send_message(chat_id, "❗️ Текст не найден.")
            return
        try:
            detected = detect(text)
            user_states[chat_id]['source_lang'] = detected
            name = LANG_CODES_TO_NAMES.get(detected, detected)
            bot.send_message(chat_id, f"🔍 Язык определён автоматически: {name}")
        except:
            bot.send_message(chat_id, "❗️ Не удалось определить язык.")
            return
        ask_target_language(chat_id)

    # Выбор целевого языка
    elif call.data in LANG_CODES_TO_NAMES:
        user_data['target_lang'] = call.data
        perform_translation(chat_id)

    # Оценка перевода
    elif call.data in ['rate_good', 'rate_bad']:
        if call.data == 'rate_bad':
            data = user_states.get(call.message.chat.id, {})
            print("👎 Пользователь недоволен переводом:")
            print(f"Текст: {data.get('text')}")
            print(f"Исходный язык: {data.get('source_lang')}")
            print(f"Целевой язык: {data.get('target_lang')}")
            print(f"Перевод: {data.get('translated')}")
        bot.answer_callback_query(call.id, "Спасибо за вашу оценку!")
        bot.send_message(call.message.chat.id, "Оценка принята 👍")

def ask_target_language(chat_id):
    bot.send_message(chat_id, "🌍 Выберите язык, на который перевести:", reply_markup=language_keyboard())

def perform_translation(chat_id):
    data = user_states.get(chat_id, {})
    text = data.get('text')
    src = data.get('source_lang', 'auto')
    tgt = data.get('target_lang')

    try:
        translated = GoogleTranslator(source=src, target=tgt).translate(text)
        data['translated'] = translated

        src_name = LANG_CODES_TO_NAMES.get(src, src)
        tgt_name = LANG_CODES_TO_NAMES.get(tgt, tgt)

        # Отправка текста
        bot.send_message(chat_id,
            f"📌 <b>Оригинал</b> ({src_name}):\n{text}\n\n"
            f"🌍 <b>Перевод</b> ({tgt_name}):\n{translated}",
            parse_mode='HTML'
        )

        # Озвучка
        tts = gTTS(translated, lang=tgt)
        filename = f"voice_{chat_id}.mp3"
        tts.save(filename)
        with open(filename, 'rb') as audio:
            bot.send_audio(chat_id, audio)
        os.remove(filename)

        # Оценка
        rating_kb = types.InlineKeyboardMarkup()
        rating_kb.add(
            types.InlineKeyboardButton("👍", callback_data='rate_good'),
            types.InlineKeyboardButton("👎", callback_data='rate_bad')
        )
        bot.send_message(chat_id, "Оцените перевод:", reply_markup=rating_kb)

    except Exception as e:
        bot.send_message(chat_id, f"❗️ Ошибка при переводе: {e}")

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
