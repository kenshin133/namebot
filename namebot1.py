
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("705992708:AAFYBJ-xaPJcRcSuwp3RYsjoDHILouDW0b0")
    global names
    names=["this","that"]

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("echo", echo))
    dp.add_handler(CommandHandler("name", name))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    temp=update.message.text
    temp=temp.split(' ')
    #update.message.reply_text("temp is " + str(temp))
    update.message.reply_text("did you say " + temp[1] + "?")

def name(bot, update):
    ##todo: move print to its own function that needs a single argument
    ##todo: print names on individual lines
    ##todo: load a database file
    ##todo: save to a database file
    global names
    #update.message.reply_text(update.message.text + " is a great name")
    temp=update.message.text
    temp=temp.split(' ')
    #update.message.reply_text("temp is " + str(temp))
    if len(temp) == 3:
        update.message.reply_text("that is a lot of arguments")
        if temp[1] == "add":
            update.message.reply_text("you want to add")
            temp2 = [temp[2]]
            update.message.reply_text("temp2 is " + str(temp2) + "names is " + str(names) + "adding now")
            names = names + temp2
            update.message.reply_text("temp2 is " + str(temp2) + "names is " + str(names))

        elif temp[1] == "print":
            update.message.reply_text(names)
    elif len(temp) == 2:
        update.message.reply_text(temp[1] + " is a great name")
    else:
        update.message.reply_text("I dont get it")
    #update.message.reply_text(temp[1] + " is a great name")

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)




if __name__ == '__main__':
    main()
