import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificacionesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'notificaciones'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Recibe mensajes enviados al grupo
    async def enviar_notificacion(self, event):
        mensaje = event['mensaje']
        await self.send(text_data=json.dumps({
            'mensaje': mensaje
        }))
