from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from .models import EventRegistration
from .form import EventForm
class EventCreateView(CreateView):
    model = EventRegistration
    template_name = 'home/event_form.html'
    form_class = EventForm
    redirect_field_name = "redirect_to"

class EventDetailView(DetailView):
    model = EventRegistration
    template_name = "home/event_form_landing.html"

from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.views.generic.usage import UsageView
from wagtail.admin.views.generic import CopyView, InspectView
from wagtail.admin.views.generic.history import HistoryView

class EventViewSet(ModelViewSet):
    model = EventRegistration
    form_fields = ["first_name", "last_name", "email", "event"]
    list_display = ["first_name", "last_name", "email", "event"]
    list_export = ["first_name", "last_name", "email", "event"]
    list_filter = ["first_name", "last_name", "email", "event"]
    menu_label = "Event Form"
    icon = "group"
    add_to_admin_menu = True
    copy_view_enabled = False
    inspect_view_enabled = True
    inspect_view_fields = ["first_name", "last_name", "email", "event"]
    usage_view_class = UsageView
    copy_view_class = CopyView
    inspect_view_class = InspectView
    history_view_class = HistoryView


event_viewset = EventViewSet("event")