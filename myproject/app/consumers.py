import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add this WebSocket to the 'dashboard' group
        await self.channel_layer.group_add("dashboard", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove this WebSocket from the 'dashboard' group
        await self.channel_layer.group_discard("dashboard", self.channel_name)

    async def update_dashboard(self, event):
        # Send the data to the WebSocket
        await self.send(json.dumps(event["data"]))
