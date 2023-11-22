import telebot
from dotenv import load_dotenv
import os
import logging
import pprint
import sys
from odoo_api import OdooRPC

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_handler = logging.StreamHandler(sys.stdout)
logger_handler.setLevel(logging.DEBUG)
logger.addHandler(logger_handler)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s')
logger_handler.setFormatter(formatter)


load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(token=TOKEN)


# Handle the /start command
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ForceReply(selective=False)
    bot.send_message(
        message.chat.id,
        '''Привет, я ваш помощник члена АКПН. Я напомню Вам о важных событиях, предложу участие в целевых группах и буду присылать ссылки на оплату членства.

Найдите свой Telegram PIN в личном кабинет на сайте АКПН https://akpn.org/my/account''',
        disable_web_page_preview=True,
        reply_to_message_id=message.message_id
    )

    bot.send_message(message.chat.id, text='Введите ваш Telegram PIN:', reply_markup=markup)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    pprint.pprint(f'Reply to: {message}')
    markup = telebot.types.ForceReply(selective=False)

    # Check if the message is a reply to a previous message with the text "Введите ваш Telegram PIN:"
    # If so, check if the 'telegram_pin' is valid and set the telegram_chat_id for the AKPN user
    if (message.reply_to_message is not None 
        and (message.reply_to_message.text == "Введите ваш Telegram PIN:" 
        or message.reply_to_message.text == "Не могу найти в базе АКПН такого участника. Проверьте PIN и попробуйте еще раз.")):
        
        try:
            telegram_pin = message.text
            logger.debug(f'PIN: {telegram_pin}')
            odoo = OdooRPC()
            #Get AKPN user by telegram_pin from Odoo
            akpn_user_record = odoo.get_odoo_user(telegram_pin)
            
            # If AKPN usert found
            if akpn_user_record:
                #And if telegram_pin is set - send a message that the user is already subscribed
                if akpn_user_record.telegram_chat_id:
                    bot.reply_to(message, text=f'{akpn_user_record.name}, вы уже подписаны на уведомления.')
                # If telegram_pin is not set - set it and send a message that the user is subscribed
                else:
                    # And set a 'telegram_chat_id' for the AKPN user
                    odoo.set_telegram_chat_id(akpn_user_record.id, message.chat.id)
                    logger.debug(f"A new telegram_chat_id {message.chat.id} set for a res.partner ID: {akpn_user_record.id}")
                    bot.reply_to(message,
                                text=f'''Нашел! Вы, {akpn_user_record.name}! Теперь я буду присылать вам важные уведомления.''')
            # If no AKPN user found - send a message that the user is not found
            else:
                bot.reply_to(message, 
                            text=f'''Не могу найти в базе АКПН такого участника. Проверьте PIN и попробуйте еще раз.''', reply_markup=markup
                            )
        except Exception as e:
            logger.debug(f'Failed to get AKPN Users from Odoo: {e}')
    else:
        pass


# Run the bot
bot.polling()


