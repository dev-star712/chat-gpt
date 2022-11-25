from django.conf import settings
from django.db import models 
import os , importlib

class BotHandler:
    def __init__(self, bot_actives):
        
        self.bot_actives = bot_actives
    
    def validate_file(self, file_name: str):
        full_path = os.path.join(settings.BASE_DIR, os.path.join('bots',file_name))
        if os.path.exists(full_path):
            return file_name
    
    def get_bot(self, command):
        for bot in self.bot_actives:
            message_handler = bot.message_handler.replace(' ','')
            if ',' in message_handler:
                for messages in message_handler.split(','):
                    if messages == command:
                        return bot 
            if message_handler == command:
                return bot 
            
    def get_execute_command(self, bot):
        file_bot = bot.file_name 

        if '.py' in file_bot:
            file_bot = file_bot.replace('.py','')

        bot_module = importlib.import_module(f'bots.{file_bot}')
        has_execute = hasattr(bot_module, 'execute_command')

        if has_execute:
            executed_command = getattr(bot_module, 'execute_command')
            return (bot, executed_command())

    def get_response(self, command):
        bot = self.get_bot(command)
        if bot and self.validate_file(bot.file_name):
            return self.get_execute_command(bot)