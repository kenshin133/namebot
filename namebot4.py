
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
##TODO alter the add method to always update a database, alter the save method to sort, merge, etc the temp db and a long term one, including archiving the old ersion and making a new one

#do your imports
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def main():
    #load names
    ##short for testing
    open_file = open('names.db.short', 'r')
    ##long for later
    ##open_file = open('names.db', 'r')
    global all_names
    all_names = open_file.readlines()

    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    file=open('apitoken.txt','r')
    filetoken=file.readline()
    token=str(filetoken).rstrip("\n\r")
    updater = Updater(token)
    global names
    names=["this","that"]

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("echo", echo))
    dp.add_handler(CommandHandler("name", name))
    dp.add_handler(CommandHandler("load", load))
    dp.add_handler(CommandHandler("save", save))

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
    ##TODO seperate the list into seperate lines
     """Send a message when the command /help is issued."""
     update.message.reply_text('I can do a few things.\n Let me know cool names with "/name somename" \n "/name add NAME" #will add the name to our database\n "/name print" #will print the names in our database\n"/help" will print this menu\n "/echo words words words" #is as close to talking as i get \n "/load" # should load the the databases but this is not used anymore \n "/save" # should save the new names to database but this has been added to the add section"')


def echo(bot, update):
    """Echo the user message."""
    temp=update.message.text
    temp=temp.split(' ')
    #update.message.reply_text("temp is " + str(temp))
    update.message.reply_text("did you say " + temp[1] + "?")

def name(bot, update):
    ##Todo: refactor so that the second argument is always checked, and subfunctions run from there
    ##todo: print names on individual lines
    ##todo: load a database file
    ##todo: save to a database file
    global names
    global all_names
    #update.message.reply_text(update.message.text + " is a great name")
    temp=update.message.text
    temp=temp.split(' ')
    #update.message.reply_text("temp is " + str(temp))
    if temp[1] == "add" and len(temp) == 3:
        temp2 = [temp[2] + "\n"]
        #names = names + temp2
        all_names = all_names + temp2
        update.message.reply_text(str(temp[2]) + " added to local database")
        save(bot,update)

    elif temp[1] == "print":
        update.message.reply_text("hardcoded ones: " + str(names) + "loaded ones : " + str(all_names))


    else:
        if len(temp) == 2:
            update.message.reply_text(temp[1] + " is a great name")
        else:
            update.message.reply_text("I dont get it")
    #    if temp[1] == "add":
    #        update.message.reply_text("you want to add")
    #        temp2 = [temp[2]]
    #        update.message.reply_text("temp2 is " + str(temp2) + "names is " + str(names) + "adding now")
    #        ##names = names + temp2
    #        update.message.reply_text("temp2 is " + str(temp2) + "names is " + str(names))

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def load(bot, update):
    #"""Echo the user message."""
    #temp=update.message.text
    #temp=temp.split(' ')
    #update.message.reply_text("temp is " + str(temp))
    update.message.reply_text(" this will load the database into memory but it is in todo status" )

def save(bot, update):
    update.message.reply_text("updating database" )
    global all_names
    with open('names.db.short','w') as f:
        for item in all_names:
            f.write("{}".format(item))
        update.message.reply_text("database updated")



if __name__ == '__main__':
    main()
