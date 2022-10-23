import telebot
from config import keys, TOKEN
from extensions import ConvertionException, MonetaryConverter


bot = telebot.TeleBot(TOKEN)                # инициализируем телебот.


@bot.message_handler(commands=['start', 'help'])        # вызов команд /start и /help
def help(message: telebot.types.Message):
    text = 'Для получения результата, напишите через пробел сумму валюты в которую хотите перевести, желаемую валюту, количество. \
\nУвидеть список всех доступных валют: /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])               # вызов команды со списком валют
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])      # обработчик сообщений и написание ответа
def convert(message: telebot.types.Message):
    try:
        a = message.text.lower()         # перевод в нижний регистр и разбиваем на части.
        values = a.split(' ')

        if len(values) > 3:
            raise ConvertionException('Слишком много параметров')
        elif len(values) < 3:
            raise ConvertionException('Слишком мало параметров')

        quote, base, amount = values
        d = MonetaryConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        result = f"{round(d['result'], 2)} {keys[base]}"
        bot.send_message(message.chat.id, result)


bot.polling()
