from django.urls import path
from wagtail import hooks

from .views import event_viewset


@hooks.register("register_admin_viewset")
def register_viewset():
    return event_viewset