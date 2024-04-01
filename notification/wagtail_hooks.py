from wagtail import hooks

from .views import notification_viewset
from django.urls import path, reverse


@hooks.register("register_admin_viewset")
def register_viewset():
    return notification_viewset

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['notification/notification.svg']