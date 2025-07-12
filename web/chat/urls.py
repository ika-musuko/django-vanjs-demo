from django.urls import include, path

import django_eventstream

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("send_message", views.send_message, name="send_message"),
]

sse_channels = ["botchunk"]
urlpatterns += [
    path(
        "_sse/botchunk/",
        include(django_eventstream.urls),
        {"channels": sse_channels},
        name="sse",
    )
]
