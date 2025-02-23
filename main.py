import os
import logging
from dataclasses import dataclass

import telebot
from telebot import types

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dataclass
class Config:
    TELEGRAM_API_TOKEN: str
    TELEGRAM_WHITE_LIST_USERS: set[int]

def load_config() -> Config:
    telegram_api_token = os.environ.get("TELEGRAM_API_TOKEN")
    if not telegram_api_token:
        raise Exception("TELEGRAM_API_TOKEN environment variable not set")

    telegram_white_list_users = os.environ.get("TELEGRAM_WHITE_LIST_USERS") or ""
    if not telegram_white_list_users:
        raise Exception("TELEGRAM_WHITE_LIST_USERS environment variable not set")

    white_list = set([int(val) for val in telegram_white_list_users.split(",") if val.isdigit()])
    if not white_list:
        raise Exception("WHITE_LIST_USERS is empty!")

    return Config(TELEGRAM_API_TOKEN=telegram_api_token, TELEGRAM_WHITE_LIST_USERS=white_list)


cfg = load_config()
bot = telebot.TeleBot(cfg.TELEGRAM_API_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    logger.debug(message.from_user.id)
    bot.send_message(message.chat.id, "Привет, для открытия шлагбаума используй команду /open")


@bot.message_handler(commands=['open'])
def handle_start(message: types.Message):
    logger.debug(message.from_user.id)
    bot.send_message(message.chat.id, "Привет, я ваш телеграм-бот!")


if __name__ == '__main__':
    bot.polling()
    logger.info("Bot started!")
