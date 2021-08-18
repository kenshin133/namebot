
#!/usr/bin/env python
# -*- coding: utf-8 -*-

###5.2 changelogs
    #added a new bot to botfather called coolnamebotbeta so i can run local instances of testing versions while also allownig the prod version to go on.
        #done
    #add "scream method" which will look for a debug variable and wither output to Telegram or to the terminal depending on the situation.
        #done but not needed since im using the beta bot
    #TODO alter debug so that it does not contact the bot at all
        #this is no longer needed since I can use the betabot
            #for this I will need another method to make sure input can be taken on the command line?
    # we would set debug when working on the bot and if we did not want our output to be sent to the bot
        #done
    #remove the "name list" mention from /help. this is handled by /list now
        #done

##INSTALLING: sudo pip install python-telegram-bot --upgrade
##also needs python3
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
##TODO alter the add method to always update a database, \
## alter the save method to sort, merge, etc the temp db and a long term one,
## including archiving the old ersion and making a new one

#do your imports
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

debugtoggle=0

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def scream(bot,update,string):
    # if debugtoggle==0:
    #     update.message.reply_text(string)
    # if debugtoggle==1:
    #     print(string)
    update.message.reply_text(string)
def main():
    #load names
    ##short for testing
    open_file = open('names.db.new', 'r')
    ##long for later
    ##open_file = open('names.db.new', 'r')
    global all_names
    all_names = open_file.readlines()
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    if debugtoggle==0:
        file=open('apitoken.txt','r')
    else:
        file=open('apitokenbeta.txt','r')
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
    dp.add_handler(CommandHandler("list", list))

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
    ##update.message.reply_text('Hi!')
    scream(bot,update,'Hi!')


def help(bot, update):
    ##TODO seperate the list into seperate lines
    """Send a message when the command /help is issued."""
    #update.message.reply_text('I can do a few things.\n'
    #   'Let me know cool names with "/name somename" \n'
    #                               ' "/name add NAME" #will add the name to our database\n '
    #                               '/help" will print this menu\n'
    #                               ' "/echo words words words" #is as close to talking as i get \n '
    #                               '"/list" will list the names and "/list e" will list all the names staring with "e"')
    #
    scream(bot,update,'I can do a few things.\n'
                               'Let me know cool names with "/name somename" \n'
                               ' "/name add NAME" #will add the name to our database\n '
                               '"/name print" #will print the names in our database\n"'
                               '/help" will print this menu\n'
                               ' "/echo words words words" #is as close to talking as i get \n '
                               '"/list" will list the names and "/list e" will list all the names staring with "e"')
def list(bot,update):
    ##TODO: list a different message if no names are found under a letter
    ##TODO: possibly change /name add to /add
    #This shouldo probably not have the first name addded immediately
    #sort the names without seperating capital and lower case.
    sorted_names = sorted(all_names, key=str.lower)

    #start the list and message no change the first name will be a duplicate
    message = str(sorted_names[0])
    message_letter = str()
    previous = [sorted_names[0]]
    #print(previous)
    #print(all_names[0])
    #print(all_names)
    ##Get letter to list specific names below
    #format
    temp = update.message.text
    temp = temp.split(' ')
    #print(temp)
    #set first argument to hopefully a letter
    #print(len(temp))
    if len(temp) > 1:
        letter=str(temp[1])
    else:
        letter="0"
    #if they selected a letter
    previous = [sorted_names[0]]
    if letter.isalpha() and len(letter) == 1:
        if previous[0][0] == letter.upper() or previous[0][0] == letter.lower():
            message_letter = message_letter + str(previous[0]).capitalize()
            #print(message_letter)

        #print("LETTER: " + letter)
        for name_temp in sorted_names:
            n = name_temp.lower()
            #print("first letter of " + n + " is " + n[0])
            if n[0] == letter.lower() or n[0] == letter.upper():
                #print(n + " matches letter")
                # print("preparing " + str(n))
                dupe = 0
                for p_temp in previous:
                    p = p_temp.lower()
                    # print("p is " + str(p))
                    if n.lower() == p.lower():
                        # print("I found dupe" + str(n) + " " + str(p))
                        dupe = 1
                        break
                # if nothing fails
                if dupe == 0:
                    previous.append(n.lower())
                    message_letter = message_letter + n.capitalize()
                    # print(previous)
                # print("finished " + str(n) + " the list is " + str(previous))
        #update.message.reply_text("Names starting with " + letter + ":\n" + message_letter)
        scream(bot,update,"Names starting with " + letter + ":\n" + message_letter)
    # print all names without any duplicates.
    # n*n checks for duplicates and if nothing matches adds it to the output.
    ##TODO: sort output perhaps
    else:
        for name_temp in sorted_names:
            #print(u"name_temp is " + (name_temp))

            n = name_temp
            #print("preparing " + str(n))
            dupe = 0
            for p in previous:
                #print("p is " + str(p))
                if n.lower() == p.lower():
                    #print("I found dupe" + str(n) + " " + str(p))
                    dupe = 1
                    break
                #else:
                    #print("i found a not dupe " + str(n))
            # if nothing fails
            if dupe == 0:
                #print("n is " + str(n))
                previous.append(n)
                message = message + n.capitalize()
                #print(previous)
            #print("finished " + str(n) + " the list is " + str(previous))
        #update.message.reply_text(message)
        scream(bot,update,message)



    ##Old method:
    # i=0
    # previous=[str(all_names[0])]
    # while i < len(all_names):
    #   comp=[all_names[i]]
    #   print(all_names[i])

    ###check for duplicate names
    # j = 0
    # dupe=0
    # while j <= len(previous):

    #    print(j)
    #    #print(comp[0])
    #    #print(comp)
    #    #print(str(comp[0]))
    #    #print(previous)
    #    #print(previous[0])
    #    #print(str(previous[j]))
    #    #print("length of previous is " + str(len(previous)))
    #    print("comparing \"" + comp[0] + "\" to \"" + previous[j] + "\"")
    #    if comp[0] == previous[j]:
    #        print("duplicate name" + str(comp[0]))
    #        dupe=1
    #        j = j + 1
    #        break

    #    else:
    #        print(str(previous[j])+ "not duplicate name " + str(comp[0]))
    #        previous = previous + comp
    #        #This was causing messages to be duplicated
    #        #message = message + all_names[i]
    #        j = j + 1
    # if dupe == 0:
    #    message= message + all_names[i]

    # i = i + 1
    # print("i is now " + str(i))
    # print(message)
    # update.message.reply_text(message)


def echo(bot, update):
    """Echo the user message."""
    temp=update.message.text
    temp=temp.split(' ')
    #update.message.reply_text("temp is " + str(temp))
    #update.message.reply_text("did you say " + temp[1] + "?")
    scream(bot,update,"did you say " + temp[1] + "?")

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
        #update.message.reply_text(str(temp[2]) + " added")
        scream(bot,update,str(temp[2]) + " added")
    #        print(str(temp[2]) + " added")
        save(bot,update)
    elif temp[1] == "print":
        list(bot,update)



    else:
        if len(temp) == 2:
            #update.message.reply_text(temp[1] + " is a great name")
            scream(bot,update,temp[1] + " is a great name")
        else:
            #update.message.reply_text("I dont get it")
            scream(bot,update,"I dont get it")
    #    if temp[1] == "add":
    #        update.message.reply_text("you want to add")
    #        temp2 = [temp[2]]
    #        update.message.reply_text("temp2 is " + str(temp2) + "names is " + str(names) + "adding now")
    #        ##names = names + temp2
    #        update.message.reply_text("temp2 is " + str(temp2) + "names is " + str(names))

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

#This is basically depricated/not in use at this time 
def load(bot, update):
    #"""Echo the user message."""
    #temp=update.message.text
    #temp=temp.split(' ')
    #update.message.reply_text("temp is " + str(temp))
    update.message.reply_text(" this will load the database into memory but it is in todo status" )

#This is basically depricated/not in use at this time
def save(bot, update):
    #update.message.reply_text("updating database" )
    global all_names
    with open('names.db.new','w') as f:
        for item in all_names:
            f.write("{}".format(item))
        #update.message.reply_text("database updated")



if __name__ == '__main__':
    main()
