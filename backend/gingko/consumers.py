# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from gingko.serializers import SubmissionSerializer
from asgiref.sync import sync_to_async
from gingko.tasks import align_sequences
from gingko.models import Result
from django.forms.models import model_to_dict

class CustomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("tasks", self.channel_name)
        print(self.channel_layer)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        action = data.get("action")
        if action == "create_submission":
            serializer = SubmissionSerializer(data=data["payload"])
            if serializer.is_valid():
                obj = await sync_to_async(serializer.save)()
                await self.send(
                    json.dumps({
                        "type": "websocket.send", 
                        "action": "new_submission", 
                        "payload": serializer.data
                    })
                )
                task = align_sequences.delay(obj.id)
                task.channel_name = self.channel_name

    async def task_complete(self, event):
        result_obj = await sync_to_async(Result.objects.get)(id=event["result"])
        payload = {
            "id": event["submission_id"],
            "initiated_on": event["initiated_on"],
            "completed_on": event["completed_on"],
            "status": event["status"],
            "result": model_to_dict(result_obj)
        } 
        await self.send(text_data=json.dumps({"type": "websocket.send", "action": "update_submission", "payload": payload}))
        