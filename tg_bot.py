import logging
import os
import sys

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow_helpers import detect_tg_intent_texts

project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
developer_chat_id = os.getenv("DEVELOPER_CHAT_ID")


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Напиши привет или задай свой вопрос')
    context.bot_data['logger'].info('Start command received')


def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    text = update.message.text

    response_text = detect_tg_intent_texts(
        project_id=project_id,
        session_id=str(user_id),
        text=text,
        language_code='ru',
    )
    update.message.reply_text(response_text)
    context.bot_data['logger'].info(f'DialogFlow response: {response_text}')


def error_handler(update: Update, context: CallbackContext) -> None:
    context.bot_data['error_logger'].error(
        msg="Exception while handling an update:", exc_info=context.error)

    try:
        context.bot.send_message(
            chat_id=developer_chat_id, text=str(context.error))
    except Exception as e:
        context.bot_data['error_logger'].error(
            f"Ошибка при отправке сообщения об ошибке: {e}")


def main() -> None:
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('activity_logger')

    error_logger = logging.getLogger('error_logger')
    error_logger.setLevel(logging.ERROR)

    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.bot_data['logger'] = logger
    dispatcher.bot_data['error_logger'] = error_logger

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, handle_message))

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
