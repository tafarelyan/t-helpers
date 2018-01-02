def create_chatbot(commands=None):
    if commands:
        func_tpl = '\ndef {func}(bot, update):\n    pass\n\n'
        functions = ''.join([func_tpl.format(func=func) for func in commands])

        handler_tpl = "    dp.add_handler(CommandHandler('{h}', {h}))\n"
        add_handlers = ''.join([handler_tpl.format(h=h) for h in commands])

    else:
        functions, add_handlers = '', ''

    with open('bot.py', 'w') as f:
        f.write(
            'from telegram.ext import Updater, CommandHandler\n\n\n'
            'def start(bot, update):\n'
            '    update.message.reply_text(\'Hello World\')\n\n'
            '{functions}\n'
            'def main():\n'
            '    updater = Updater("TOKEN")\n'
            '    dp = updater.dispatcher\n\n'
            '    dp.add_handler(CommandHandler(\'start\', start))\n'
            '{add_handlers}\n'
            '    updater.start_polling()\n'
            '    updater.idle()\n\n\n'
            'if __name__ == \'__main__\':\n'
            '    main()\n'
            .format(functions=functions, add_handlers=add_handlers)
        )
