from django.db import models


class Message(models.Model):
    type = models.CharField(max_length=50)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]


class ChatHistory(models.Model):
    session_id = models.CharField(max_length=100)
    messages = models.ManyToManyField(Message)
