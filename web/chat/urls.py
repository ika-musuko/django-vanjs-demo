from django.urls import include, path

import django_eventstream

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("send_message", views.send_message, name="send_message")
]

sse_channels = ["reply"]
urlpatterns += [
    path(
        "_sse/reply/",
        include(django_eventstream.urls),
        {"channels": sse_channels},
        name="sse",
    )
]
