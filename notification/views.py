from django.shortcuts import render

# Create your views here.
from .models import Notification
from wagtail.admin.viewsets.model import ModelViewSet
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class NotificationViewSet(ModelViewSet):
    model = Notification
    form_fields = ["title", "message", "receiver"]
    icon = "notification"
    add_to_admin_menu = True
    copy_view_enabled = True
    inspect_view_enabled = True
    # add_to_settings_menu = True


notification_viewset = NotificationViewSet("notification")  # defines /admin/notification/ as the base URL

class NotificationView(LoginRequiredMixin, ListView):
    model = Notification
    paginate_by = 100  # if pagination is desired
    login_url = "authentication:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notification.objects.all()
        context["notifications"] = notifications
        return context