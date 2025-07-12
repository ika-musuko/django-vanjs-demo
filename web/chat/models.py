from django.contrib import admin
from django.db import models


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=128)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    pass


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    text = models.TextField()
    from_user = models.BooleanField()

    conversation = models.ForeignKey(  # many to one
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
