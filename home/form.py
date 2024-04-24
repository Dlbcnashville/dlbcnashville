from django import forms
from .models import EventRegistration
from wagtail.admin.forms.models import WagtailAdminModelForm

class EventForm(WagtailAdminModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['event'].widget.attrs.update({'placeholder': 'Select event'})
   
    class Meta:
        model = EventRegistration
        fields = ('first_name', 'last_name', 'email', 'event')