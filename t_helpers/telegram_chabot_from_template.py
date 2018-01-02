import os

TEMPLATES = os.path.join(os.path.dirname(__file__), 'templates')


def create_basic_chatbot(commands=None):

    if commands:
        func_tpl = '\ndef {func}(bot, update):\n    pass\n\n'
        functions = ''.join([func_tpl.format(func=func) for func in commands])

        handler_tpl = "dp.add_handler(CommandHandler('{h}', {h}))\n"
        add_handlers = '    '.join([handler_tpl.format(h=h) for h in commands])

    else:
        functions, add_handlers = '', ''

    with open(os.path.join(TEMPLATES, 'basic.tpl'), 'r') as f:
        template = f.read().format(functions=functions, add_handlers=add_handlers)

    with open('bot.py', 'w') as f:
        f.write(template)
