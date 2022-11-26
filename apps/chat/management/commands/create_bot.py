from django.core.management.base import BaseCommand
from apps.chat.models import Bot
from django.contrib.auth.models import User 
from django.conf import settings

import random, string, os
class Command(BaseCommand):
    
    def handle(self, *args, **options):
        bot_username = input('Username for your bot : ')
        file_name = input('File name to generate : ')
        description = input('Bot Description : ')
        message_handler = input('Message Handler (e.g : /hello,/fush,/foo) : ')

        if 'bot' not in bot_username:
            bot_username = f'bot_{bot_username}'

        dirname = os.path.dirname(file_name)
        if dirname:
            file_name = file_name.replace(dirname,'')
        
        if '.py' not in file_name:
            file_name = f'{file_name}.py'
        
        file_name = os.path.join(settings.BOT_DIR, file_name)
        if os.path.exists(file_name):
            choose = input(f'{file_name} exists, do you want to rewrite it (y/n) ? : ')
            if choose.lower() != 'y':
                return 
    
        file_content = """
def execute_command():
    return "Change this response!"

        """
        with open(file_name, 'w') as file:
            file.write(file_content)
        
        self.stdout.write(f'File created {file_name}')
        # generate user for bot
        
        user, created = User.objects.get_or_create(username=bot_username)
        if not created:
            self.stdout.write('Bot username already exist, create another one!')
            return 
        user.set_password(''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(random.randint(10,16))))
        user.save()

        self.stdout.write('User for bot created!')
        
        b = Bot(user=user, file_name=file_name, description=description, message_handler=message_handler)
        b.save()