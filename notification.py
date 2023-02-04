__author__ = "Lavanya Naresh"
__modified__ = "04-Feb-2023"

import os
import logging
from telegram import Bot
from telegram import ParseMode
from telegram.error import TelegramError
from dotenv import load_dotenv

from strategy import *
from utility.parameter_dataclasses import *

"""
objective:
Basically a logger
It notifies when the certain condition as stated in strategy.py is satisfied.

STEPS:
1. get the data from adapter.py for the NSE LTP
2. using that LTP data check, make arithmetic operations with strategy.py
3. check for the condition fulfilment.
4. notify if condition fulfilled then timeout else timeout directly
5. repeat loop
"""

# setup env vars
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_notification(message, chat_id):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    try:
        bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        logging.error("Failed to send notification to Telegram: {}".format(e))


def notification(data: data_basemodel) -> int:
    """
    Function
    Helper function that takes input data and makes decision to send notification

    Params
    ------
    data: pydantic.basemodel
        input data
        Example:
            {
                "position": class_order_object_yet_to_be_created,
                "ltp": float,
                "mtm": float,
                "what needs to be done": IDK,
                "addi_notes": Optional[list[str]] | Optional[str]
            }

    Returns
    -------
    result: int
        Should the output be bool? I think it should be integer (one hot encoding kind of results)
        1 -> put
        2 -> call
        3 -> neutral
        ...
        1 to N where N is the possible number of decisions that can be taken at a position
    """
    result = None
    # some code here that does the required tasks
    return result
