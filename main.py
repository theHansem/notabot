import os
import logging
from replit import db

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

from telegram import Update #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)

from math import ceil
from flask import render_template
from flask import Flask
app = Flask(__name__)
@app.route('/')
@app.route('/<int:page>')

def home(page=None):
    ks = sorted(map(int, db.keys()))
    pages = ceil(len(ks) / 10)
    if page is None: #Default to latest page
        page = pages
    if page < pages:
        next_page = page + 1
    else:
        next_page = None
    if page > 1:
        prev_page = page - 1
    else:
        prev_page = None
    messages = tuple(db[str(key)] for key in ks[(page-1)*10:page*10])

    return render_template('home.html', messages=messages, next_page=next_page, page=page, prev_page=prev_page)

def latest_key():
    ks = db.keys()
    if len(ks):
        return max(map(int, ks))
    else:
        return -1

def help_command(update: Update, context: CallbackContext) -> None:
    htext = '''
Welcome
Send a message to store it.
Send /fetch to retrieve the most recent message'''
    update.message.reply_text(htext)

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def whoami(update, context):
    """Send a message when the command /whoami is issued."""
    name = update.message.from_user.username
    update.message.reply_text('You are ' + name)

def log(update: Update, context: CallbackContext) -> None:
    db[str(latest_key() + 1)] = update.message.text

def fetch(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(db.get(str(latest_key()), 'No Messages Yet.'))

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():

    """Get the bot token from env"""
    updater = Updater(os.getenv("TOKEN"),use_context=True)
    """Create the dispatcher"""
    dispatcher = updater.dispatcher
    """Dispatcher Commands"""
    dispatcher.add_handler(CommandHandler("start", help_command))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("fetch", fetch))
    dispatcher.add_handler(CommandHandler("whoami", whoami))
    dispatcher.add_handler(CommandHandler("echo", echo))
    """Dispatcher non-Commands"""
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, log))


    dispatcher.add_error_handler(error)

    updater.start_polling()

    app.run(host='0.0.0.0', port=8080, debug=True)
    updater.idle()

if __name__ == '__main__':
    main()