import logging
import os
import sys

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(stream=sys.stdout, level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
error_logger = logging.getLogger('error_logger')

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
activity_logger = logging.getLogger('activity_logger')


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я эхобот.')
    activity_logger.info('Start command received')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)
    activity_logger.info(f'Message echoed: {update.message.text}')


def error_handler(update: Update, context: CallbackContext) -> None:
    error_logger.error(
        msg="Exception while handling an update:", exc_info=context.error)


def main() -> None:
    updater = Updater(token, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
