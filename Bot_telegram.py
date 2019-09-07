import telebot

TOKEN = '961357837:AAFIzY0yeqaw_0zz-KBu1z7aAIXnCVbf8ws'
bot = telebot.TeleBot(TOKEN)

def send_match(match_info, url_ifo):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Больше информации', url=url_ifo))
    bot.send_message(chat_id=716536607, text=str(match_info), reply_markup=keyboard)
    bot.send_message(chat_id=931880445, text=str(match_info), reply_markup=keyboard)
# send_match("Запуск")
