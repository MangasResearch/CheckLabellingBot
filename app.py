#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SELECT = 1

imgs = ['https://www.abc.net.au/tv/common/images/publicity/ZX9129A_460.jpg',
        'https://images.discordapp.net/avatars/366632492590956544/e33fb154663f5a63138d934224b47c7d.png?size=512',
        'https://img1.ak.crunchyroll.com/i/spire4/589007d48b5162ef3625c4660537ae461508803872_large.jpg',
        'https://cdn.ome.lt/vJh7iUeM-avxLHbX7xbZ8Ar-3X8=/1200x630/smart/extras/conteudos/anime-dr-stone-head.jpg']
count = 0

def start(update, context):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                InlineKeyboardButton("Option 2", callback_data='2')],

            [InlineKeyboardButton("Option 3", callback_data='3')]]

    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    context.bot.send_photo(chat_id=update.message.chat_id, 
        photo='https://telegram.org/img/t_logo.png',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return SELECT


def gender(update, context): 
    global count
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                InlineKeyboardButton("Option 2", callback_data='2')],

            [InlineKeyboardButton("Option 3", callback_data='3')]]

    query = update.callback_query
    context.bot.delete_message(chat_id=query.message.chat_id,
                               message_id=query.message.message_id)

    context.bot.send_photo(chat_id=query.message.chat_id, 
        photo=imgs[count],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    count += 1

    if count >= len(imgs):
        count = 0

    return SELECT


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("TOKEN HERE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SELECT: [CallbackQueryHandler(gender)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    print("Pressione CTRL+C para cancelar")
    main()
