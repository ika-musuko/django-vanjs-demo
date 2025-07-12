from django.urls import include, path

import django_eventstream

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_conversation", views.new_conversation, name="new_conversation"),
    path("get_conversation_messages/<int:conversation_id>", views.get_conversation_messages, name="get_conversation_messages"),
    path("delete_conversation/<int:conversation_id>", views.delete_conversation, name="delete_conversation"),
    path("send_message", views.send_message, name="send_message"),
]

urlpatterns += [
    path("_sse/<channel>", include(django_eventstream.urls)),
]
