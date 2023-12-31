from dotenv import load_dotenv, find_dotenv
import os
from datetime import datetime
import odoorpc
import json
from logger import logger
import pprint



class OdooRPC:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv("ODOO_HOST")
        self.port = os.getenv("ODOO_PORT")
        self.database = os.getenv("ODOO_DB")
        self.username = os.getenv("ODOO_USERNAME")
        self.password = os.getenv("ODOO_PWD")
        self.odoo = None
    
    def connect(self):
        try:
            self.odoo = odoorpc.ODOO(self.host, port=self.port)
            self.odoo.login(self.database, self.username, self.password)
            return self.odoo
        except Exception as e:
            logger.debug(f'Failed to connect to Odoo: {e}')

    # Find a 'res.user' in Odoo by telegram_pin. Return his records if found one
    def get_odoo_user(self, telegram_pin):
        try:
            odoo = self.connect()
            domain = [('telegram_pin', '=', telegram_pin)]
            akpn_user_id = odoo.env['res.partner'].search(domain)
            if akpn_user_id:
                logger.debug(f'Found AKPN user: {akpn_user_id}')
                akpn_user_record = odoo.env['res.partner'].browse(akpn_user_id)
                logger.debug(f'AKPN user name: {akpn_user_record.name}')
                return akpn_user_record
            else:
                logger.debug(f'AKPN user not found')

        except Exception as e:
            logger.debug(f'Failed to get AKPN Users from Odoo: {e}')

    # Set 'telegram_chat_id' passed from Telebot to a 'res.user' in Odoo
    def set_telegram_chat_id(self, partner_id, telegram_chat_id):
        try:
            odoo = self.connect()
            domain = [('id', '=', partner_id)]
            akpn_user_id = odoo.env['res.partner'].search(domain)
            if akpn_user_id:
                logger.debug(f'Found AKPN user: {akpn_user_id}')
                partner = odoo.env['res.partner'].browse(akpn_user_id)
                # Set 'telegram_chat_id' for the AKPN user
                telegram_chat_id = partner.write({'telegram_chat_id': telegram_chat_id})
                return telegram_chat_id
            else:
                logger.debug(f'AKPN user not found')

        except Exception as e:
            logger.debug(f'Failed to get AKPN Users from Odoo: {e}')

    # Create a new 'telebot.group' record in Odoo within a given 'telegram_chat_id', 'chat_title' and 'chat_type'
    # Before creating a new record check if the 'telegram_chat_id' already exists in Odoo
    def create_telegram_group(self, telegram_chat_id, chat_title, chat_type):
        try:
            odoo = self.connect()
            get_tg_group = odoo.env['telebot.group'].search([('telegram_chat_id', '=', telegram_chat_id)])
            if not get_tg_group:
                # Create a new 'telegram.group' record in Odoo
                new_group = odoo.env['telebot.group'].create({
                    'telegram_chat_id': telegram_chat_id,
                    'name': chat_title,
                    'type': chat_type,
                })
                logger.debug(f'New telegram.group created: {chat_title}, {new_group}')
                return new_group
            else:
                logger.debug(f'Telegram group already exists. Odoo ID: {get_tg_group}')
                return get_tg_group
        except Exception as e:
            logger.debug(f'Failed to create a new telegram.group: {e}')