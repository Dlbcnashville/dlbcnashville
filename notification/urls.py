from django.urls import path
from notification.views import NotificationView

app_name = "notification"

urlpatterns = [
    path("notifications/", NotificationView.as_view(), name="notification_list"),
]