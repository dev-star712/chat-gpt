from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

layer = get_channel_layer()

async def send_message(message, group_room_code):
    await layer.group_send(group_room_code, 
          {
                "message":message,
                "type":"bot.response",
                "sender":"bot_response",
        }
    )
