with open("key.txt") as f:
    TOKEN = f.read()
import json
import time

from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup
import time as t

from Entry import on_calendar, on_request, CallbackQueryHandler, on_callback_query
#from Start import start
from Commands import commands
from Site import site
from Price import price
from Stopping import stop


def helper(update, context):
    if update.message.text == "РАСЧЕТ":
        return 1
    if update.message.text == "/calendar":
        return 2

reply_keyboard = [['/price', '/stop'],
                  ['/site', '/calendar']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def start(update, context):
    update.message.reply_text(
        "Я бот-помошник. Я могу записать Вас на приём \
        в наш автосервис или подсказать когда вам назначено \
        посещение  \
        для ознакомления со всем моим функционалом Вы можете ввести комманду \
        /commands \
        Так же я могу произвести примерный расчёт стоимости работ \
        для этого вам необходимо прислать название работы в виде словосочетания \
        например: окраска бампера \
        при необходимости выполнения более одной позиции названия надо разделять запятой и пробелом \
        если желаете начаь расчёт пришлите слово РАСЧЕТ",

        reply_markup=markup
    )


def main():
    # Создаём объект updater.
    updater = Updater(TOKEN, use_context=True)
    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # Регистрируем обработчик в диспетчере.
    dp.add_handler(CommandHandler('calendar', on_calendar))
    dp.add_handler(CommandHandler("price", price))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CallbackQueryHandler(on_callback_query))
    #dp.add_handler(CommandHandler("entry", entry))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("commands", commands))
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[MessageHandler(Filters.text, helper)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, price)],
            2: [MessageHandler(Filters.text & ~Filters.command, on_request)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    #text_handler = text_handler = MessageHandler(Filters.text, on_request)

    dp.add_handler(conv_handler)
    #dp.add_handler(text_handler)
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()


    # Ждём завершения приложения.
    updater.idle()

if __name__ == '__main__':
    main()
