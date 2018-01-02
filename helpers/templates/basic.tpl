from telegram.ext import Updater, CommandHandler


def start(bot, update):
    update.message.reply_text('Hello World')

{functions}
def main():
    updater = Updater("TOKEN")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    {add_handlers}
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
