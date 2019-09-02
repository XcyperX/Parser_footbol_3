import telebot

TOKEN = '961357837:AAFIzY0yeqaw_0zz-KBu1z7aAIXnCVbf8ws'
bot = telebot.TeleBot(TOKEN)

def send_match(match_info):
    bot.send_message(chat_id=716536607, text=str(match_info))
    bot.send_message(chat_id=931880445, text=str(match_info))
send_match("Запуск")
# @bot.message_handler(commands=['start'])
# def start_command(message):
#     bot.send_message(
#         message.chat.id,
#         'Greetings! I can show you exchange rates.\n' +
#         'To get the exchange rates press /exchange.\n' +
#         'To get help press /help.' +
#         send_match()
#   )

# bot.polling(none_stop=True)