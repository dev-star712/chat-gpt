from django.conf import settings
from django.db import models 
import os , importlib

class BotHandler:
    def __init__(self, bot_actives, group_room_code):
        
        self.bot_actives = bot_actives
        self.group_room_code = group_room_code
    
    async def validate_file(self, file_name: str):
        full_path = os.path.join(settings.BASE_DIR, os.path.join('bots',file_name))
        if os.path.exists(full_path):
            return file_name
    
    async def get_bot(self, command):
        for bot in self.bot_actives:
            message_handler = bot.message_handler.replace(' ','')
            if ',' in message_handler:
                for messages in message_handler.split(','):
                    if messages == command:
                        return bot 
            if message_handler == command:
                return bot 
            
    async def get_execute_command(self, bot, argument: list):
        file_bot = bot.file_name 

        if '.py' in file_bot:
            file_bot = file_bot.replace('.py','')

        bot_module = importlib.import_module(f'bots.{file_bot}')
        has_execute = hasattr(bot_module, 'execute_command')

        if has_execute:
            executed_command = getattr(bot_module, 'execute_command')
            return (bot, await executed_command(argument, group_room_code=self.group_room_code))

    async def get_response(self, command):
        command_splitted = command.split(' ')

        if len(command_splitted) > 1:
            command, *argument = command_splitted
        else:
            command, argument = (command_splitted[0], [])
        
        bot = await self.get_bot(command)
        if bot and await self.validate_file(bot.file_name):
            return await self.get_execute_command(bot, argument)